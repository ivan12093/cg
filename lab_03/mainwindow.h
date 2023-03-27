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
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QColor getPenColor() const;
    Domain::Line getLine() const;
    Domain::Spectre getSpectre() const;
    QString getDrawAlgo() const;

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

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
