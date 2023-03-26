#include "mainwindow.h"
#include "app.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    auto app = App(&w);
    return a.exec();
}
