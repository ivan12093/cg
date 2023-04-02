#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "domain/line.h"
#include "domain/spectre.h"

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

private:
    QColor pen_color = QColor(Qt::black);

public:
    enum DrawAlgo {Default, CDA, BresenhamInteger, BresenhamFloat,
                  BresenhamSmooth, Wu};
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QColor getPenColor() const;
    Domain::Line getLine() const;
    Domain::Spectre getSpectre() const;
    DrawAlgo getDrawAlgo() const;

    Ui::MainWindow *getUi() const;
signals:
    void drawLineRequested();
    void drawSpectreRequested();
    void undo();
    void clearCanvas();
private slots:
    void on_pickColorPushButton_clicked();
    void on_colorPicked(const QColor &color);
    void on_backgroundColorPicked(const QColor &color);
    void on_undoAction_triggered();
    void on_pickBackgroundColorPushButton_clicked();
    void on_clearCanvasAction_triggered();
    void on_increaseScalePushButton_clicked();
    void on_dereaseScalePushButton_clicked();
    void on_authorAction_triggered();
    void on_timeAction_triggered();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
