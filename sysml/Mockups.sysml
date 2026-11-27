/*
 * Мокапы окон приложения SecureBooking (бронирование переговорных
 * с шифрованием персональных данных).
 * Каждое окно — отдельный пакет с одной частью типа UiKit::Window.
 * PNG-изображения строятся из этой модели: python docs/tools/sysml2png.py
 */
package SecureBooking_UI {

    /* Окно 1. Вход (UC-02; REQ-FUNC-003, REQ-SEC-005). */
    package LoginMockup {
        private import UiKit::*;

        part loginWindow : Window {
            attribute :>> title = "SecureBooking — вход";

            part body : Row {
                part leftGap : Column;
                part loginCard : Card {
                    attribute :>> weight = 2;
                    attribute :>> text = "Вход в систему";
                    part hint : Label {
                        attribute :>> text = "Бронирование переговорных";
                        attribute :>> style = TextStyle::muted;
                    }
                    part login : TextField {
                        attribute :>> label = "Логин";
                        attribute :>> text = "petrov";
                    }
                    part password : PasswordField {
                        attribute :>> label = "Пароль";
                        attribute :>> text = "••••••••••";
                    }
                    part error : Label {
                        attribute :>> text = "Неверный логин или пароль";
                        attribute :>> style = TextStyle::warning;
                    }
                    part buttons : Row {
                        part signIn : Button {
                            attribute :>> text = "Войти";
                            attribute :>> primary = true;
                        }
                        part register : Button {
                            attribute :>> text = "Регистрация";
                        }
                    }
                    part privacy : Label {
                        attribute :>> text = "ФИО, телефон и e-mail хранятся в зашифрованном виде";
                        attribute :>> style = TextStyle::muted;
                    }
                }
                part rightGap : Column;
            }
        }
    }

    /* Окно 2. Регистрация (UC-01; REQ-FUNC-001, REQ-FUNC-002, REQ-SEC-001). */
    package RegistrationMockup {
        private import UiKit::*;

        part registrationWindow : Window {
            attribute :>> title = "SecureBooking — регистрация";

            part body : Row {
                part formCard : Card {
                    attribute :>> weight = 3;
                    attribute :>> text = "Новая учётная запись";
                    part credentials : Row {
                        part login : TextField {
                            attribute :>> label = "Логин";
                            attribute :>> text = "ivanov";
                        }
                        part password : PasswordField {
                            attribute :>> label = "Пароль (от 8 символов)";
                            attribute :>> text = "••••••••••";
                        }
                        part passwordRepeat : PasswordField {
                            attribute :>> label = "Повтор пароля";
                            attribute :>> text = "••••••••••";
                        }
                    }
                    part fullName : TextField {
                        attribute :>> label = "ФИО";
                        attribute :>> text = "Иванов Иван Иванович";
                    }
                    part contacts : Row {
                        part phone : TextField {
                            attribute :>> label = "Телефон";
                            attribute :>> text = "+375 29 765-43-21";
                        }
                        part email : TextField {
                            attribute :>> label = "E-mail";
                            attribute :>> text = "i.ivanov@company.by";
                        }
                    }
                    part buttons : Row {
                        part submit : Button {
                            attribute :>> text = "Зарегистрироваться";
                            attribute :>> primary = true;
                        }
                        part cancel : Button {
                            attribute :>> text = "Отмена";
                        }
                        part gap : Column;
                    }
                }
                part privacyCard : Card {
                    attribute :>> weight = 2;
                    attribute :>> text = "Защита данных";
                    part p1 : Label {
                        attribute :>> text = "ФИО, телефон и e-mail шифруются AES-256-GCM.";
                    }
                    part p2 : Label {
                        attribute :>> text = "Пароль хранится только как хеш PBKDF2.";
                    }
                    part p3 : Label {
                        attribute :>> text = "Другие сотрудники видят «Фамилия И. О.»";
                    }
                    part p4 : Label {
                        attribute :>> text = "и маскированный телефон.";
                    }
                    part p5 : Label {
                        attribute :>> text = "Первый пользователь — администратор.";
                        attribute :>> style = TextStyle::muted;
                    }
                }
            }
        }
    }

    /* Окно 3. Главное окно сотрудника (UC-03, UC-04, UC-05; REQ-FUNC-004…007, REQ-SEC-007). */
    package MainMockup {
        private import UiKit::*;

        part mainWindow : Window {
            attribute :>> title = "SecureBooking — бронирование переговорных";

            part menu : MenuBar {
                attribute :>> items = ("Файл", "Профиль", "Администрирование", "Справка");
                attribute :>> disabled = ("Администрирование");
                attribute :>> user = "Петров П. И. · сотрудник";
            }
            part stats : Row {
                part freeNow : StatCard {
                    attribute :>> label = "Свободно сейчас";
                    attribute :>> text = "2 из 3";
                }
                part myToday : StatCard {
                    attribute :>> label = "Мои брони на 14.11";
                    attribute :>> text = "2";
                }
                part next : StatCard {
                    attribute :>> label = "Ближайшая встреча";
                    attribute :>> text = "11:00 · Альфа";
                }
            }
            part rooms : Row {
                part alpha : RoomCard {
                    attribute :>> text = "Альфа";
                    attribute :>> info = "10 мест · 3 этаж · проектор";
                    attribute :>> status = RoomStatus::free;
                    attribute :>> note = "свободна до 11:00";
                    attribute :>> selected = true;
                }
                part beta : RoomCard {
                    attribute :>> text = "Бета";
                    attribute :>> info = "6 мест · 3 этаж · ТВ-панель";
                    attribute :>> status = RoomStatus::busy;
                    attribute :>> note = "занята до 11:00";
                }
                part gamma : RoomCard {
                    attribute :>> text = "Гамма";
                    attribute :>> info = "16 мест · 5 этаж · видеосвязь";
                    attribute :>> status = RoomStatus::free;
                    attribute :>> note = "свободна весь день";
                }
            }
            part work : Row {
                part scheduleCard : Card {
                    attribute :>> weight = 3;
                    attribute :>> text = "Расписание: Альфа, 14.11.2026";
                    part filters : Row {
                        part room : ComboBox {
                            attribute :>> text = "Альфа (10 мест)";
                        }
                        part date : DateField {
                            attribute :>> text = "14.11.2026";
                        }
                    }
                    part schedule : Table {
                        attribute :>> columns = ("Время", "Организатор", "Телефон", "Цель встречи");
                        part r1 : TableRow { attribute :>> cells = ("08:00–09:00", "свободно", "", ""); }
                        part r2 : TableRow { attribute :>> cells = ("09:00–10:00", "Сидорова А. С.", "+375 ** ***-**-67", "Планёрка отдела"); }
                        part r3 : TableRow { attribute :>> cells = ("10:00–11:00", "свободно", "", ""); }
                        part r4 : TableRow {
                            attribute :>> cells = ("11:00–12:30", "Петров Пётр Иванович", "+375447654321", "Встреча с заказчиком");
                            attribute :>> selected = true;
                        }
                        part r5 : TableRow { attribute :>> cells = ("12:30–14:00", "свободно", "", ""); }
                        part r6 : TableRow { attribute :>> cells = ("14:00–16:00", "Аксак В. С.", "+375 ** ***-**-33", "Защита проекта"); }
                        part r7 : TableRow { attribute :>> cells = ("16:00–20:00", "свободно", "", ""); }
                    }
                }
                part bookingPanel : Card {
                    attribute :>> weight = 2;
                    attribute :>> text = "Новое бронирование";
                    part times : Row {
                        part start : ComboBox {
                            attribute :>> label = "Начало";
                            attribute :>> text = "16:00";
                        }
                        part end : ComboBox {
                            attribute :>> label = "Окончание";
                            attribute :>> text = "17:00";
                        }
                    }
                    part purpose : TextField {
                        attribute :>> label = "Цель встречи";
                        attribute :>> text = "Обсуждение требований";
                    }
                    part book : Button {
                        attribute :>> text = "Забронировать";
                        attribute :>> primary = true;
                    }
                    part cancel : Button {
                        attribute :>> text = "Отменить своё бронирование";
                    }
                    part rules : Label {
                        attribute :>> text = "08:00–20:00, шаг 30 мин, не более 4 ч";
                        attribute :>> style = TextStyle::muted;
                    }
                    part privacy : Label {
                        attribute :>> text = "Телефоны других сотрудников скрыты";
                        attribute :>> style = TextStyle::muted;
                    }
                }
            }
        }
    }

    /* Окно 4. Мои бронирования (UC-06; REQ-FUNC-007). */
    package MyBookingsMockup {
        private import UiKit::*;

        part myBookingsWindow : Window {
            attribute :>> title = "SecureBooking — мои бронирования";

            part menu : MenuBar {
                attribute :>> items = ("Файл", "Профиль", "Администрирование", "Справка");
                attribute :>> disabled = ("Администрирование");
                attribute :>> user = "Петров П. И. · сотрудник";
            }
            part bookingsCard : Card {
                attribute :>> text = "Мои бронирования";
                part bookings : Table {
                    attribute :>> columns = ("Дата", "Время", "Переговорная", "Цель встречи");
                    part r1 : TableRow {
                        attribute :>> cells = ("14.11.2026", "11:00–12:30", "Альфа", "Встреча с заказчиком");
                        attribute :>> selected = true;
                    }
                    part r2 : TableRow { attribute :>> cells = ("14.11.2026", "10:00–11:00", "Бета", "Собеседование"); }
                    part r3 : TableRow { attribute :>> cells = ("15.11.2026", "13:00–14:00", "Гамма", "Ретроспектива спринта"); }
                }
                part actions : Row {
                    part cancel : Button {
                        attribute :>> text = "Отменить выбранное";
                    }
                    part gap : Column {
                        attribute :>> weight = 2;
                    }
                    part close : Button {
                        attribute :>> text = "Закрыть";
                    }
                }
            }
        }
    }

    /* Окно 5. Администрирование: переговорные (UC-08; REQ-FUNC-008). */
    package RoomsMockup {
        private import UiKit::*;

        part roomsWindow : Window {
            attribute :>> title = "SecureBooking — переговорные";

            part menu : MenuBar {
                attribute :>> items = ("Файл", "Профиль", "Администрирование", "Справка");
                attribute :>> user = "Аксак В. С. · администратор";
            }
            part body : Row {
                part listCard : Card {
                    attribute :>> weight = 3;
                    attribute :>> text = "Переговорные";
                    part rooms : Table {
                        attribute :>> columns = ("Название", "Мест", "Этаж", "Оборудование");
                        part r1 : TableRow { attribute :>> cells = ("Альфа", "10", "3", "проектор, маркерная доска"); }
                        part r2 : TableRow {
                            attribute :>> cells = ("Бета", "6", "3", "ТВ-панель");
                            attribute :>> selected = true;
                        }
                        part r3 : TableRow { attribute :>> cells = ("Гамма", "16", "5", "видеосвязь, проектор"); }
                    }
                    part delete : Button {
                        attribute :>> text = "Удалить выбранную";
                    }
                }
                part newRoomCard : Card {
                    attribute :>> weight = 2;
                    attribute :>> text = "Новая переговорная";
                    part name : TextField {
                        attribute :>> label = "Название";
                        attribute :>> text = "Дельта";
                    }
                    part numbers : Row {
                        part capacity : TextField {
                            attribute :>> label = "Мест";
                            attribute :>> text = "8";
                        }
                        part floor : TextField {
                            attribute :>> label = "Этаж";
                            attribute :>> text = "4";
                        }
                    }
                    part equipment : TextField {
                        attribute :>> label = "Оборудование";
                        attribute :>> text = "маркерная доска";
                    }
                    part add : Button {
                        attribute :>> text = "Добавить";
                        attribute :>> primary = true;
                    }
                }
            }
        }
    }

    /* Окно 6. Администрирование: пользователи (UC-09; REQ-FUNC-010). */
    package UsersMockup {
        private import UiKit::*;

        part usersWindow : Window {
            attribute :>> title = "SecureBooking — пользователи";

            part menu : MenuBar {
                attribute :>> items = ("Файл", "Профиль", "Администрирование", "Справка");
                attribute :>> user = "Аксак В. С. · администратор";
            }
            part stats : Row {
                part total : StatCard {
                    attribute :>> label = "Пользователей";
                    attribute :>> text = "3";
                }
                part admins : StatCard {
                    attribute :>> label = "Администраторов";
                    attribute :>> text = "1";
                }
                part encrypted : StatCard {
                    attribute :>> label = "Зашифрованных полей ПД";
                    attribute :>> text = "9 из 9";
                }
            }
            part usersCard : Card {
                attribute :>> text = "Пользователи (данные расшифрованы для администратора)";
                part users : Table {
                    attribute :>> columns = ("ID", "Логин", "Роль", "ФИО", "Телефон", "E-mail");
                    part r1 : TableRow { attribute :>> cells = ("1", "admin", "Администратор", "Аксак Владислав Сергеевич", "+375291112233", "v.aksak@bsuir.by"); }
                    part r2 : TableRow { attribute :>> cells = ("2", "petrov", "Сотрудник", "Петров Пётр Иванович", "+375447654321", "p.petrov@company.by"); }
                    part r3 : TableRow { attribute :>> cells = ("3", "sidorova", "Сотрудник", "Сидорова Анна Сергеевна", "+375251234567", "a.sidorova@company.by"); }
                }
                part note : Label {
                    attribute :>> text = "На диске эти данные хранятся только в зашифрованном виде";
                    attribute :>> style = TextStyle::muted;
                }
            }
        }
    }

    /* Окно 7. Администрирование: зашифрованное хранилище (UC-10; REQ-SEC-001, REQ-SEC-002). */
    package StorageMockup {
        private import UiKit::*;

        part storageWindow : Window {
            attribute :>> title = "SecureBooking — хранилище";

            part menu : MenuBar {
                attribute :>> items = ("Файл", "Профиль", "Администрирование", "Справка");
                attribute :>> user = "Аксак В. С. · администратор";
            }
            part storageCard : Card {
                attribute :>> text = "Файл booking.db на диске";
                part legend : Label {
                    attribute :>> text = "Поля ФИО, телефона и e-mail — шифртекст AES-256-GCM; строка MAC — контрольная сумма файла";
                    attribute :>> style = TextStyle::muted;
                }
                part content : CodeBlock {
                    attribute :>> lines = (
                        "SECUREBOOKING-DB|1",
                        "ROOM|1|Альфа|10|3|проектор, маркерная доска",
                        "USER|1|admin|admin|q8Vd2K…|Xy7pL0…|kD93nf…|3Fh9Zq1mT0p8…|bR42xNw0uK…|Lm07sQe2Vt…",
                        "USER|2|petrov|user|Hc1oPa…|R0z8Wd…|aP61cj…|9xVt2LmQe7r…|Zt5Nq0pW3a…|Ue8kR1fXd4…",
                        "BOOK|2|1|2|2026-11-14|660|750|Встреча с заказчиком",
                        "MAC|p/TkSF2RCdKDFRuNw5GCf+hA6ILI8gJhead6/wJ9kFZ="
                    );
                }
                part paths : Row {
                    part db : Label {
                        attribute :>> text = "Ключи: master.key (защищены DPAPI)";
                        attribute :>> style = TextStyle::muted;
                    }
                    part close : Button {
                        attribute :>> text = "Закрыть";
                    }
                }
            }
        }
    }
}
