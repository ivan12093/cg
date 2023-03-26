#ifndef APP_H
#define APP_H

#include <stack>
#include <QObject>

#include "mainwindow.h"
#include "domain/command.h"

class App : public QObject
{
    Q_OBJECT
private:
    MainWindow *main_window = nullptr;
    std::stack<Domain::Command*> command_stack;
public:
    explicit App(MainWindow *mw);
    ~App();
public slots:
    void on_drawLineRequest();
    void on_drawSpectreRequest();
    void on_undo();
};

#endif // APP_H
