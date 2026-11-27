package SecureBooking_UseCases {
    doc /* Действующие лица и варианты использования системы SecureBooking
         * (защищённая система бронирования переговорных).
         * Автор: Аксак В. С., гр. 434701. */

    // ---------- Система и действующие лица ----------
    part def SecureBookingSystem {
        doc /* Настольное приложение Windows для бронирования переговорных. */
    }
    part def Employee {
        doc /* Сотрудник: бронирует переговорные, управляет своими данными. */
    }
    part def Administrator :> Employee {
        doc /* Администратор: дополнительно управляет переговорными и пользователями. */
    }

    // ---------- Варианты использования ----------
    use case def Authenticate {
        doc /* UC-02. Вход по логину и паролю. */
        subject system : SecureBookingSystem;
        actor user : Employee;
    }

    use case def Register {
        doc /* UC-01. Регистрация: логин, пароль, ФИО, телефон, e-mail.
             * ФИО, телефон и e-mail сохраняются в зашифрованном виде. */
        subject system : SecureBookingSystem;
        actor user : Employee;
    }

    use case def ViewSchedule {
        doc /* UC-03. Просмотр занятых и свободных интервалов переговорной на дату. */
        subject system : SecureBookingSystem;
        actor user : Employee;
        include use case auth : Authenticate;
    }

    use case def BookRoom {
        doc /* UC-04. Бронирование переговорной на свободный интервал. */
        subject system : SecureBookingSystem;
        actor user : Employee;
        objective {
            doc /* Переговорная закреплена за сотрудником без пересечения с другими бронями. */
        }
        include use case schedule : ViewSchedule;
    }

    use case def CancelBooking {
        doc /* UC-05. Отмена своего бронирования (администратор — любого). */
        subject system : SecureBookingSystem;
        actor user : Employee;
        include use case auth : Authenticate;
    }

    use case def ViewMyBookings {
        doc /* UC-06. Список собственных бронирований. */
        subject system : SecureBookingSystem;
        actor user : Employee;
        include use case auth : Authenticate;
    }

    use case def EditPersonalData {
        doc /* UC-07. Изменение своих ФИО, телефона, e-mail и пароля. */
        subject system : SecureBookingSystem;
        actor user : Employee;
        include use case auth : Authenticate;
    }

    use case def ManageRooms {
        doc /* UC-08. Добавление и удаление переговорных. */
        subject system : SecureBookingSystem;
        actor admin : Administrator;
        include use case auth : Authenticate;
    }

    use case def ViewUsers {
        doc /* UC-09. Просмотр пользователей с расшифрованными персональными данными. */
        subject system : SecureBookingSystem;
        actor admin : Administrator;
        include use case auth : Authenticate;
    }

    use case def AuditStorage {
        doc /* UC-10. Просмотр файла хранилища: проверка, что ПД зашифрованы. */
        subject system : SecureBookingSystem;
        actor admin : Administrator;
        include use case auth : Authenticate;
    }
}
