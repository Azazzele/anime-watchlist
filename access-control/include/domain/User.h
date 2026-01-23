#ifndef USER_H
#define USER_H

#include <string>
#include <ctime>

/**
 * @class User
 * @brief Представляет пользователя системы с уникальным ID, именем и временем создания.
 */
class User {
private:
    int id;
    std::string name;
    std::time_t createdAt;

public:
    /**
     * @brief Конструктор пользователя
     * @param id Уникальный идентификатор пользователя
     * @param name Имя пользователя (не должно быть пустым)
     */
    User(int id, const std::string& name);

    /**
     * @brief Получает ID пользователя
     * @return Идентификатор пользователя
     */
    int getId() const;

    /**
     * @brief Получает имя пользователя
     * @return Имя пользователя
     */
    const std::string& getName() const;

    /**
     * @brief Получает время создания пользователя
     * @return Время создания в формате time_t
     */
    std::time_t getCreatedAt() const;

    /**
     * @brief Устанавливает имя пользователя
     * @param name Новое имя пользователя
     */
    void setName(const std::string& name);
};

#endif // USER_H
