/*
 * UiKit — библиотека элементов интерфейса для прототипирования окон
 * настольного приложения SecureBooking на SysML v2.
 *
 * Окно описывается деревом частей (part): контейнеры (Row, Column, Card)
 * задают компоновку, остальные элементы — поля, кнопки, таблицы и карточки.
 * Изображения строятся скриптом docs/tools/sysml2png.py.
 */
package UiKit {
    private import ScalarValues::*;

    enum def TextStyle {
        enum title;
        enum normal;
        enum muted;
        enum warning;
    }

    enum def RoomStatus {
        enum free;
        enum busy;
    }

    /* Базовый элемент интерфейса. */
    abstract part def Widget {
        /* Отображаемый текст: надпись, заголовок или пример значения. */
        attribute text : String [0..1];
        /* Относительная ширина элемента внутри строки (Row). */
        attribute weight : Integer = 1;
    }

    /* Контейнер: размещает вложенные элементы. */
    abstract part def Container :> Widget {
        part children : Widget [0..*];
    }

    /* Окно приложения Windows. */
    part def Window :> Container {
        attribute title : String;
    }

    /* Строка: элементы располагаются слева направо. */
    part def Row :> Container;

    /* Колонка: элементы располагаются сверху вниз; пустая колонка — отступ. */
    part def Column :> Container;

    /* Карточка: контейнер с рамкой, тенью и необязательным заголовком text. */
    part def Card :> Container;

    /* Главное меню окна. */
    part def MenuBar :> Widget {
        attribute items : String [0..*];
        attribute disabled : String [0..*];
        attribute user : String [0..1];
    }

    part def Label :> Widget {
        attribute style : TextStyle = TextStyle::normal;
    }

    /* Поле ввода: label — подпись над полем, text — пример значения. */
    part def TextField :> Widget {
        attribute label : String [0..1];
    }
    part def PasswordField :> TextField;
    part def DateField :> TextField;
    part def ComboBox :> TextField;

    part def Button :> Widget {
        attribute primary : Boolean = false;
    }

    /* Карточка показателя: label — название, text — значение. */
    part def StatCard :> Widget {
        attribute label : String;
    }

    /* Карточка переговорной: text — название, info — вместимость и этаж. */
    part def RoomCard :> Widget {
        attribute info : String;
        attribute status : RoomStatus = RoomStatus::free;
        attribute note : String [0..1];
        attribute selected : Boolean = false;
    }

    part def TableRow :> Widget {
        attribute cells : String [0..*];
        attribute selected : Boolean = false;
    }

    part def Table :> Widget {
        attribute columns : String [1..*];
        part rows : TableRow [0..*];
    }

    /* Блок моноширинного текста (содержимое файла). */
    part def CodeBlock :> Widget {
        attribute lines : String [0..*];
    }
}
