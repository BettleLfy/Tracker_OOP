class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, 
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories


    def get_message(self):
        
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: float = 60
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20
    
    def get_spent_calories(self):
        result_running_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))
        return result_running_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: int = 2
    coeff_calorie_5: float = 0.029 
    
    def __init__(self, 
                action: int, 
                duration: float, 
                weight: float,
                height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        result_sportswalking_calories = ((self.coeff_calorie_3 * self.weight
                + (self.get_mean_speed() ** self.coeff_calorie_4 // self.height)
                * self.coeff_calorie_5 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))
        return result_sportswalking_calories

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_6: float = 1.1
    coeff_calorie_7: int = 2
    
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
                                    + self.coeff_calorie_6)
                                    * self.coeff_calorie_7 
                                    * self.weight)
        return result_swimming_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict_training[workout_type](*data)


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

