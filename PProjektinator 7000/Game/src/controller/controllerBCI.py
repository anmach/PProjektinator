from pyOpenBCI import wifi as bci
import tensorflow as tf
import src.define as define
from scipy.fftpack import fftfreq


def car(sample, all_samples):
    return sample - all_samples.mean()


def frequency_range(min_freq, max_freq, freq_values):
    min_index = 0
    max_index = 0
    while freq_values[max_index] < max_freq:
        if freq_values[min_index] < min_freq:
            min_index += 1
        max_index += 1
    return min_index, max_index


def ambient_freq(signal, frequencies, step):
    average = np.zeros(step)
    count = 0

    i = step
    length = len(signal)
    progress = 0
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{date} {round(progress * 100)}% done")
    while i < length:
        if sum1d(frequencies[i - step:i]) == 0:
            average = np.add(average, np.abs(fft(signal[i - step:i])))
            count += 1
        if i / length > progress:
            progress += 0.1
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            print(f"{date} {round(progress * 100)}% done")
        i += step
    return average / count


def normalize(y):
    y_norm = np.zeros(len(y))

    factor = 1.0 / np.max(y)
    for i, x in enumerate(y):
        if x < 0:
            y_norm[i] = 0
        else:
            y_norm[i] = factor * y[i]
    return y_norm


def non_zero_freq_test(signal, frequencies, step, s):
    i = s + step if s is not None else step
    length = len(signal)

    while i < length:
        if sum(frequencies[i - step:i]) >= 0.6 * step:
            return np.abs(fft(signal[i - step:i])), i
        i += step
    return None, None


def prepare_data(sample):
    signal1 = sample[5]
    signal2 = sample[6]
    car_signal1 = list(map(car, signal1, all_probes))
    car_signal2 = list(map(car, signal2, all_probes))
    freq_values = fftfreq(2000, 0.001)

    (minIndex, maxIndex) = frequency_range(8, 20, freq_values)
    ambient_freq_pow1 = ambient_freq(car_signal1[0:], frequencies[0:], 2000)
    ambient_freq_pow2 = ambient_freq(car_signal2[0:], frequencies[0:], 2000)
    y_background1 = ambient_freq_pow1[minIndex:maxIndex]
    y_background2 = ambient_freq_pow2[minIndex:maxIndex]
    y_avg_background = (y_background1 + y_background2) / 2

    x_data = list()
    s = 0
    while s is not None:
        y1, s = non_zero_freq_test(car_signal1[s:], frequencies[s:], 2000, s)
        y2, _ = non_zero_freq_test(car_signal2[s:], frequencies[s:], 2000, s)

        if y1 is not None and y2 is not None:
            y1 = y1[minIndex:maxIndex]
            y2 = y2[minIndex:maxIndex]
            y_avg = np.add(y1, y2)
            y_avg /= 2
            ysr_avg = np.subtract(y_avg, y_avg_background)
            ysr_avg = normalize(ysr_avg)
            x_data.append(ysr_avg)

    x_data = np.array(x_data)
    return x_data


class ControllerBCI:
    """ Kontroler do czytania myśli """

    def __init__(self, ip_address):
        self.__instructions = []
        self.__brain = tf.keras.models.load_model(define.get_brain_model())

        sample_rate = 1000
        self.shield = bci.OpenBCIWiFi(ip_address=ip_address, log=True, high_speed=True, sample_rate=sample_rate, latency=100)

    def start_reading(self):
        self.shield.start_streaming(self.printData)
        self.shield.loop()

    def stop_reading(self):
        self.shield.stop()

    def process_data(self, sample):
        if len(sample.channel_data) != 16:
            return

        temp = str(sample.channel_data)
        in_data = temp[1:len(temp) - 1]
        # przetworzenie myśli
        data = prepare_data(in_data)
        instruction = self.__brain.predict(data)
        self.__instructions.append(instruction)

    def get_instructions(self):
        inst = self.__instructions.pop(0)
        return inst
