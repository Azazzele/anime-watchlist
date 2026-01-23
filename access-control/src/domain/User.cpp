#include "User.h"
#include <stdexcept>
#include <ctime>

/**
 * @brief Конструктор класса User.
 *
 * Инициализирует пользователя с уникальным идентификатором, именем
 * и автоматически устанавливает время создания аккаунта.
 *
 * @param id Уникальный идентификатор пользователя (должен быть > 0)
 * @param name Имя пользователя (не должно быть пустым)
 *
 * @throws std::invalid_argument если id <= 0 или name пустое
 */
User::User(int id, const std::string& name)
    : id(id),
      name(name),
      createdAt(std::time(nullptr)) // фиксируем момент создания пользователя
{
    // Проверка корректности идентификатора
    if (id <= 0)
        throw std::invalid_argument("ID должен быть больше 0");

    // Проверка корректности имени
    if (name.empty())
        throw std::invalid_argument("Имя не может быть пустым");
}

/**
 * @brief Возвращает уникальный идентификатор пользователя.
 *
 * @return ID пользователя
 */
int User::getId() const {
    return id;
}

/**
 * @brief Возвращает имя пользователя.
 *
 * @return Константная ссылка на строку с именем пользователя
 */
const std::string& User::getName() const {
    return name;
}

/**
 * @brief Возвращает время создания аккаунта.
 *
 * Время хранится в формате std::time_t и может быть
 * отформатировано при необходимости на уровне представления.
 *
 * @return Время создания пользователя
 */
std::time_t User::getCreatedAt() const {
    return createdAt;
}

/**
 * @brief Изменяет имя пользователя.
 *
 * @param name Новое имя пользователя (не должно быть пустым)
 *
 * @throws std::invalid_argument если имя пустое
 */
void User::setName(const std::string& name) {
    if (name.empty()) {
        throw std::invalid_argument("Имя не может быть пустым");
    }
    this->name = name;
}
