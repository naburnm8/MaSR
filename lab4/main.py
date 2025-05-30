import numpy as np

class Unit:
    def __init__(self, name: str, max_health: int,
                 attack_damage: int, block_value: int, heal_value: int):
        self.name = name
        self.max_health = max_health
        self.attack_damage = attack_damage
        self.block_value = block_value
        self.heal_value = heal_value
        self.health = max_health
        self.blocking = False

    def attack(self, target: "Unit") -> int:
        raw = self.attack_damage
        if target.blocking:
            damage = max(raw - target.block_value, 0)
            target.blocking = False
        else:
            damage = raw

        target.health = max(target.health - damage, 0)
        return damage

    def block(self):
        self.blocking = True

    def heal(self) -> int:
        old = self.health
        self.health = min(self.health + self.heal_value, self.max_health)
        return self.health - old

    def is_dead(self) -> bool:
        return self.health <= 0

    def status(self) -> str:
        return f"{self.name}: HP={self.health}/{self.max_health}"


class UnitBot(Unit):
    ACTIONS = ['attack', 'block', 'heal']

    def __init__(self, name, max_health,
                 attack_damage, block_value, heal_value,
                 transition_matrix: np.ndarray):
        super().__init__(name, max_health, attack_damage,
                         block_value, heal_value)
        assert transition_matrix.shape == (3,3), "Матрица 3×3"

        assert np.allclose(transition_matrix.sum(axis=1), 1.0), \
            "Сумма вероятностей в каждой строке = 1"
        self.transition_matrix = transition_matrix
        self.state = 0  # начинаем с атаки

    def next_action(self) -> str:
        probs = self.transition_matrix[self.state]
        self.state = np.random.choice([0,1,2], p=probs)
        return UnitBot.ACTIONS[self.state]


class UnitPlayer(Unit):
    def choose_action(self) -> str:
        while True:
            print("\nВыберите действие:")
            print("  1 – Атаковать")
            print("  2 – Блокировать")
            print("  3 – Восстановить здоровье")
            choice = input("Ваш выбор (1/2/3): ").strip()
            if choice == '1':
                return 'attack'
            if choice == '2':
                return 'block'
            if choice == '3':
                return 'heal'
            print("Некорректный ввод, повторите.")


def main():
    # Настройки по варианту 18 (индивидуальное задание):
    # max_health произвольное, например 100
    # attack_damage > block_value
    # heal_value ≤ max_health/2
    PLAYER_NAME = "Игрок"
    BOT_NAME    = "Бот-Марков"

    MAX_HEALTH   = 100
    ATTACK_DMG   = 20
    BLOCK_VALUE  = 10    # < ATTACK_DMG
    HEAL_VALUE   = 40    # ≤ MAX_HEALTH/2

    # Три уровня сложности: матрицы переходов
    # Лёгкий (бот чаще восстанавливается):       атака=0.5, блок=0.2, лечение=0.3
    # Средний (бот обычно атакует):              атака=0.7, блок=0.2, лечение=0.1
    # Сложный (очень агрессивный бот):           атака=0.8, блок=0.1, лечение=0.1
    mats = {
        '1': np.array([[0.5, 0.2, 0.3]]*3),
        '2': np.array([[0.7, 0.2, 0.1]]*3),
        '3': np.array([[0.8, 0.1, 0.1]]*3),
    }

    print("Выберите уровень сложности бота:")
    print("  1 – Лёгкий")
    print("  2 – Средний")
    print("  3 – Сложный")
    lvl = None
    while lvl not in mats:
        lvl = input("Уровень (1/2/3): ").strip()

    bot = UnitBot(
        BOT_NAME, MAX_HEALTH,
        ATTACK_DMG, BLOCK_VALUE, HEAL_VALUE,
        transition_matrix=mats[lvl]
    )
    player = UnitPlayer(
        PLAYER_NAME, MAX_HEALTH,
        ATTACK_DMG, BLOCK_VALUE, HEAL_VALUE
    )

    print("\n=== Игра началась! ===")
    print("Первым ходит бот (атака).\n")

    turn = 'bot'
    while not bot.is_dead() and not player.is_dead():
        if turn == 'bot':
            action = bot.next_action()
            print(f"[Бот]: {action.upper()}")
            if action == 'attack':
                dmg = bot.attack(player)
                print(f"  Бот атакует, наносит {dmg} урона.")
            elif action == 'block':
                bot.block()
                print("  Бот готовится заблокировать следующий удар.")
            elif action == 'heal':
                rec = bot.heal()
                print(f"  Бот восстанавливает {rec} HP.")
            turn = 'player'
        else:
            print(f"[{player.status()}]  [{bot.status()}]")
            action = player.choose_action()
            print(f"[Игрок]: {action.upper()}")
            if action == 'attack':
                dmg = player.attack(bot)
                print(f"  Вы атакуете, наносите {dmg} урона.")
            elif action == 'block':
                player.block()
                print("  Вы готовитесь заблокировать следующий удар.")
            elif action == 'heal':
                rec = player.heal()
                print(f"  Вы восстанавливаете {rec} HP.")
            turn = 'bot'
        print()

    if bot.is_dead() and player.is_dead():
        print("Ничья! Оба юнита пали.")
    elif bot.is_dead():
        print("Поздравляем – вы победили бота!")
    else:
        print("К сожалению, бот победил вас.")

if __name__ == "__main__":
    main()
