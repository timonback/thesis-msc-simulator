import logging
import math
from decimal import Decimal

from simulator.configuration import Configuration
from simulator.resource.instance_creator import InstanceCreator
from simulator.resource.instance_vm import InstanceVm
from simulator.resource.pricing import Pricing

logger = logging.getLogger(__name__)


class InstanceCreatorVm(InstanceCreator):
    """
    Creates Vm instances to handle an amount of requests
    """

    def __init__(self, config: Configuration):
        InstanceCreator.__init__(self)
        self.config = config
        self.pricing = Pricing(Pricing.CONFIG_VM)

    def create_instances(self, provisioned: list, start: int, requests: list) -> list:
        """
        Handles the requests incoming at start using the specified provisioned instances
        If min_instances is set to non-zero, then the amount of min_instances is guranteed when requests are coming.
        If auto_scaling is enabled in the config, additional instances are automatically added
        :param provisioned: list of Instances that are provisioned
        :param start: The time when the instances will be created (related to the incoming time of the request
        :param requests: The requests
        :return: list of *newly* created instances
        """
        unhandable_requests = list()
        unhandled_requests = self.queued
        [unhandled_requests.append(item) for item in requests]
        #unhandled_requests.extend(requests)
        if len(unhandled_requests) is 0:
            return list()

        logger.debug('Will handle {len} requests ({queue} queued, {new} new)'
                     .format(len=len(unhandled_requests), queue=len(self.queued), new=len(requests)))

        # sort list to handle long running requests first to max-out the utilization
        unhandled_requests.sort(key=lambda x: x.duration)

        memory_max = max(unhandled_requests, key=lambda x: x.memory).memory
        #memory_needed = self.config.vm_parallel * memory_max
        cost, memory, btu, dynamic = self.pricing.get_vm_price()

        new_instances = self._ensure_min_instances(provisioned, start, btu, memory, cost)
        provisioned.extend(new_instances)
        active = self._active_instances_at(start, provisioned)

        # let provision instances handle the requests
        for instance_index, instance_entry in enumerate(active):
            instance = instance_entry['instance']
            instance_requests_active = instance_entry['active_requests']

            degradation = math.pow(1 - self.config.vm_scaling_degradation, instance_index)
            instance_handable = int(max(1, degradation * self.config.vm_parallel))
            logger.debug('Instance {id} handles {active}/{len})'
                         .format(id=instance.id, active=instance_requests_active, len=instance_handable))
            if instance_requests_active >= instance_handable:
                continue

            for request in unhandled_requests[:]:
                if instance_requests_active < instance_handable:
                    if instance.handle(request):
                        instance_requests_active = instance_requests_active + 1
                        unhandled_requests.remove(request)
                        logger.debug('Instance {id} handles another request (id: {rid}) (total now: {a})'
                                     .format(id=instance.id, rid=request.id,
                                             a=instance.handling_requests_at(start)))

                        if len(unhandled_requests) is 0:
                            break

        # add instances to handle requests if auto_scaling
        if self.config.vm_auto_scaling is True:
            logger.debug('Adding new auto-scaling instance')

            instance = None  # create only an instance, if a request can be handled
            degradation = 1
            instance_handable = 0
            for request in unhandled_requests[:]:
                could_handled = InstanceVm.could_handle(start, btu, memory_max, request)
                if could_handled:
                    # a request is handleble, ensure the existence of an instance
                    if instance is None:
                        instance = InstanceVm(start, btu, memory_max, cost)
                        new_instances.append(instance)
                        degradation = math.pow(1 - self.config.vm_scaling_degradation, len(active) + len(new_instances))
                        instance_handable = int(max(1, degradation * self.config.vm_parallel))
                    if instance.handling_requests_at(start) < instance_handable:
                        is_handled = instance.handle(request)
                        if is_handled:
                            logger.debug('Instance {id} handles request (id: {rid})'
                                         .format(id=instance.id, rid=request.id))
                            if instance.handling_requests_at(start) >= instance_handable:
                                instance = None
                        else:
                            raise RuntimeError('Logic Error. A request that could_handle can not be '
                                               'is_handled?')
                    else:
                        raise RuntimeError('Logic Error. Instance is unable to handle more requests.')
                else:
                    unhandable_requests.append(request)
                unhandled_requests.remove(request)

        # rebuild the queue
        self._rebuild_queue(unhandled_requests + unhandable_requests)

        return new_instances

    def _rebuild_queue(self, unhandled_requests):
        self.queued = list()
        self.queued.extend(unhandled_requests)
        logger.debug('The queue has {len} items now'.format(len=len(self.queued)))


    def _active_instances_at(self, timestamp: int, instances: list) -> list:
        """
        Filteres the instances to only the ones that are still active at timestamp
        :param timestamp: The timestamp to check for
        :param provisioned_list: The instances to check
        :return: list of dicts. The key for the instance in the dict is instance, along with the active_requests key
        for the amount of active requests
        """
        active = list()
        for instance in instances:
            if instance.start <= timestamp and timestamp < instance.end:
                active.append({
                    'instance': instance,
                    'active_requests': instance.handling_requests_at(timestamp)
                })
        return active

    def _ensure_min_instances(self, instances: list, start: int, btu: int, max_memory: int, cost: Decimal) -> list:
        """
        Looking at the instances in instances, the amount of instances is increased to min_instances using the
        parameters for the instance.
        The start point of the instances (and point to check for the active ones) is start
        :param instances: Already running instances
        :param start: The time to check for the instances and point to start the new ones
        :param btu: The billing interval per instance
        :param max_memory: The maximum amount of memory per instance
        :param cost: The instance cost per billing unit
        :return: A list of the *newly* created instances
        """
        new_instances = list()

        active = self._active_instances_at(start, instances)
        for i in range(len(active), self.config.vm_min_instances):
            instance = InstanceVm(start, btu, max_memory, cost)
            new_instances.append(instance)
        logger.debug('Force adding {len} instances to fulfill min_instances'.format(len=len(new_instances)))
        return new_instances
