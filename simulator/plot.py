import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from simulator.resource.instance import InstanceTypes
from simulator.simulator_result import SimulatorResult


def plot(result: SimulatorResult, requests: list, filename: str):
    instance_types = result.instances_types

    plt.clf()
    fig, axes = plt.subplots(2, 1)
    xvalues = range(0, len(result.cost_steps))

    # First chart
    ax1 = axes[0]
    ax1.set_title(filename)
    ax1.set_xlabel('Time in seconds')
    ax1.plot(xvalues, result.cost_steps, c='b', label='Cost')
    label = ax1.set_ylabel('Cost in USD')
    label.set_color('b')

    # instances
    instances_total_steps = list()
    instances_faas = 0
    instances_vm = 0
    instances_faas_steps = list()
    instances_vm_steps = list()
    for instances_step in result.instances:
        for instance in instances_step:
            if instance.type == InstanceTypes.TYPE_VM:
                instances_vm = instances_vm + 1
            else:
                instances_faas = instances_faas + 1
        instances_total_steps.append(instances_faas + instances_vm)
        instances_faas_steps.append(instances_faas)
        instances_vm_steps.append(instances_vm)

    ax2 = ax1.twinx()
    ax2.plot(xvalues, instances_total_steps, c='r')
    label = ax2.set_ylabel('Total Instances', color='r')
    label.set_color('r')
    if InstanceTypes.TYPE_FAAS in instance_types and InstanceTypes.TYPE_VM in instance_types:
        ax2.plot(xvalues, instances_faas_steps, c='y', label='FaaS')
        ax2.plot(xvalues, instances_vm_steps, c='tab:orange', label='VM')
        ax2.legend()

    # Next chart
    ax1 = axes[1]
    ax1.set_xlabel('Time in seconds')
    request_lens = list(map(lambda x: len(x), requests))
    ax1.plot(xvalues, request_lens, c='b')
    label = ax1.set_ylabel('New Requests')
    label.set_color('b')

    queued_lens = list(map(lambda x: len(x), result.queued))
    if len(set(queued_lens)) is not 1:
        ax2 = ax1.twinx()
        ax2.plot(xvalues, queued_lens, c='r')
        label = ax2.set_ylabel('Queued Requests', color='r')
        label.set_color('r')

    path = '{filename}.png'.format(filename=filename)
    plt.savefig(path)
    plt.close(path)

    # show for debugging
    # plt.show()

    return path
