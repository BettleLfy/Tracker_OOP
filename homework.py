from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Метод возвращает строку сообщения."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result_dist_in_km = self.action * self.LEN_STEP / self.M_IN_KM
        return result_dist_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result_avg_speed = self.get_distance() / self.duration
        return result_avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        result_run_calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                               - self.COEFF_CALORIE_2) * self.weight
                               / self.M_IN_KM
                               * (self.duration * self.MIN_IN_HOUR))
        return result_run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: int = 2
    COEFF_CALORIE_5: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        result_sprtwalking_calories = ((self.COEFF_CALORIE_3 * self.weight
                                       + (self.get_mean_speed()
                                        ** self.COEFF_CALORIE_4 // self.height)
                                       * self.COEFF_CALORIE_5 * self.weight)
                                       * (self.duration * self.MIN_IN_HOUR))
        return result_sprtwalking_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_6: float = 1.1
    COEFF_CALORIE_7: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        result_mean_speed_swimming = (self.length_pool
                                      * self.count_pool
                                      / self.M_IN_KM
                                      / self.duration)
        return result_mean_speed_swimming

    def get_spent_calories(self) -> float:
        result_swimming_calories = ((Swimming.get_mean_speed(self)
                                    + self.COEFF_CALORIE_6)
                                    * self.COEFF_CALORIE_7
                                    * self.weight)
        return result_swimming_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    try:
        return dict_training[workout_type](*data)
    except KeyError:
        print(f'KeyError: {dict_training} '
              '- данной тренировки не найдено.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
