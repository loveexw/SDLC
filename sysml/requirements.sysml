package SecureBooking_Requirements {
    doc /* Бизнес-требования и ключевые требования к системе SecureBooking.
         * Полные формулировки — в docs/srs.md. */

    private import ScalarValues::*;

    // ---------- Бизнес-требования ----------
    requirement def <'BR'> BusinessRequirement {
        doc /* Цель заказчика, ради которой создаётся система. */
    }

    requirement businessRequirements : BusinessRequirement {
        requirement <'BR-01'> noConflicts : BusinessRequirement {
            doc /* Исключить двойные бронирования одной переговорной на одно и то же время. */
        }
        requirement <'BR-02'> protectPersonalData : BusinessRequirement {
            doc /* Персональные данные сотрудников (ФИО, телефон, e-mail) не должны раскрываться
                 * при утечке или копировании файлов системы. */
        }
        requirement <'BR-03'> selfService : BusinessRequirement {
            doc /* Сотрудник бронирует переговорную самостоятельно, без обращения к офис-менеджеру,
                 * не более чем за 1 минуту. */
        }
        requirement <'BR-04'> controlForAdmin : BusinessRequirement {
            doc /* Администратор управляет перечнем переговорных и видит контакты организаторов встреч. */
        }
        requirement <'BR-05'> lowCost : BusinessRequirement {
            doc /* Внедрение без серверов и платных лицензий на рабочих местах с Windows 10/11. */
        }
    }

    // ---------- Функциональные требования ----------
    requirement <'REQ-FUNC-001'> registration {
        doc /* Система должна регистрировать пользователя по логину, паролю, ФИО, телефону и e-mail. */
    }
    requirement <'REQ-FUNC-005'> bookingRules {
        doc /* Бронирование возможно с 08:00 до 20:00 с шагом 30 минут, не более 4 часов,
             * не ранее текущего момента и не позднее чем через 30 дней. */
        attribute durationMin : Integer;
        attribute maxDurationMin : Integer = 240;
        require constraint { durationMin <= maxDurationMin }
    }
    requirement <'REQ-FUNC-006'> noOverlap {
        doc /* Интервалы бронирований одной переговорной в одну дату не должны пересекаться. */
    }

    requirement <'REQ-FUNC-008'> manageRooms {
        doc /* Администратор должен добавлять и удалять переговорные (название, вместимость, этаж, оборудование). */
    }

    // ---------- Требования безопасности ----------
    requirement <'REQ-SEC-001'> encryptPersonalData {
        doc /* ФИО, телефон и e-mail должны храниться на диске только в зашифрованном виде
             * (AES-256-GCM). */
    }
    requirement <'REQ-SEC-003'> passwordHashing {
        doc /* Пароли должны храниться только в виде стойкого хеша с солью (PBKDF2-HMAC-SHA256). */
    }
    requirement <'REQ-SEC-007'> maskForeignData {
        doc /* Сотрудник должен видеть ФИО других сотрудников в сокращённом виде,
             * а их телефоны — маскированными. */
    }

    // ---------- Ограничения ----------
    requirement <'REQ-PORT-001'> windowsDesktop {
        doc /* Система должна работать на Windows 10/11 x64 без сервера и сторонних платных компонентов. */
    }

    // ---------- Трассировка ----------
    dependency from businessRequirements::noConflicts to noOverlap;
    dependency from businessRequirements::protectPersonalData to encryptPersonalData;
    dependency from businessRequirements::protectPersonalData to passwordHashing;
    dependency from businessRequirements::protectPersonalData to maskForeignData;
    dependency from businessRequirements::selfService to bookingRules;
    dependency from businessRequirements::selfService to registration;
    dependency from businessRequirements::controlForAdmin to manageRooms;
    dependency from businessRequirements::lowCost to windowsDesktop;

    satisfy registration by SecureBooking_UI::RegistrationMockup::registrationWindow;
    satisfy bookingRules by SecureBooking_UI::MainMockup::mainWindow.work.bookingPanel;
    satisfy maskForeignData by SecureBooking_UI::MainMockup::mainWindow.work.scheduleCard.schedule;
    satisfy encryptPersonalData by SecureBooking_UI::StorageMockup::storageWindow;
    satisfy manageRooms by SecureBooking_UI::RoomsMockup::roomsWindow;
}
