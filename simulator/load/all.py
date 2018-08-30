from .load_constant import LoadGeneratorConstant
from .load_generator import LoadGenerator
from .load_ndist import LoadGeneratorNDist
from .load_sawtooth import LoadGeneratorSawtooth
from .load_sinusoid import LoadGeneratorSinusoid
from .load_square import LoadGeneratorSquare
from .load_triangle import LoadGeneratorTriangle


class Loads:
    @staticmethod
    def get_load(config) -> LoadGenerator:
        key = config.load_name
        if key == 'constant':
            return LoadGeneratorConstant(config.load_altitude, config.load_spacing)
        if key == 'ndist':
            return LoadGeneratorNDist(config.load_altitude, config.load_spacing, config.load_num_requests,
                                      config.load_num_spikes)
        if key == 'sawtooth':
            return LoadGeneratorSawtooth(config.load_altitude, config.load_spacing)
        if key == 'sinusoid':
            return LoadGeneratorSinusoid(config.load_altitude, config.load_spacing)
        if key == 'square':
            return LoadGeneratorSquare(config.load_altitude, config.load_spacing)
        if key == 'triangle':
            return LoadGeneratorTriangle(config.load_altitude, config.load_spacing)
        raise ValueError('Load name specified in the config does not exist ({})'.format(config.load_name))
