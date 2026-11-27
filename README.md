# TaskTracker

Учебный проект по дисциплине **«Жизненный цикл разработки программного обеспечения»**
(БГУИР, кафедра ЭВМ, специальность 6-05-0611-05 «Компьютерная инженерия»).

**Автор:** Аксак В. С., группа 434701

## О проекте

TaskTracker — настольное приложение для Windows для учёта личных задач:
создание, редактирование и удаление задач, сроки и приоритеты, отметка о
выполнении, фильтрация и сохранение списка в локальный файл.

Проект разрабатывается по итеративной модели жизненного цикла: требования
(SRS), проектирование (SDD, ADR), реализация, тестирование.

## Технологии

- C++17
- Visual Studio 2022 (MSVC, toolset v143)
- Git / GitHub

## Структура репозитория

```
.
├── TaskTracker.sln            # решение Visual Studio
├── TaskTracker/
│   ├── TaskTracker.vcxproj    # проект C++
│   └── src/main.cpp           # точка входа
├── srs/  sdd/  adr/  docs/    # шаблоны документации курса
└── README.md
```

## Сборка

1. Открыть `TaskTracker.sln` в Visual Studio 2022.
2. Выбрать конфигурацию `Debug | x64`.
3. Собрать: *Build → Build Solution* (`Ctrl+Shift+B`).

Из командной строки (Developer Command Prompt):

```
msbuild TaskTracker.sln /p:Configuration=Release /p:Platform=x64
```

## Документация

Шаблоны SRS, SDD и ADR взяты из учебного репозитория
[BSUIR-SDLC/SDLC](https://github.com/BSUIR-SDLC/SDLC).
