#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "domain/command.h"

#include "math.h"

#include <iostream>
#include <QPalette>
#include <QColorDialog>
#include <QMessageBox>
#include <chrono>
#include <QtCharts/QChartView>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QLegend>
#include <QtCharts/QBarCategoryAxis>
#include <QtCharts/QValueAxis>
#include <QtCharts/QLineSeries>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , pen_color(Qt::black)
{
    ui->setupUi(this);

    // connect signals
    QObject::connect(ui->drawLinePushButton, &QAbstractButton::clicked, this, &MainWindow::drawLineRequested);
    QObject::connect(ui->drawSpectrePushButton, &QAbstractButton::clicked, this, &MainWindow::drawSpectreRequested);

    ui->graphicsView->setScene(new QGraphicsScene());
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pickColorPushButton_clicked()
{
    auto color_dialog = new QColorDialog(this);
    color_dialog->show();
    QObject::connect(color_dialog, &QColorDialog::colorSelected, this, &MainWindow::on_colorPicked);
}

void MainWindow::on_colorPicked(const QColor &color)
{
    pen_color = color;

    QString qss = QString("background-color: %1").arg(color.name());
    ui->colorFrame->setStyleSheet(qss);
}

Ui::MainWindow *MainWindow::getUi() const
{
    return ui;
}

QColor MainWindow::getPenColor() const
{
    return pen_color;
}

Domain::Line MainWindow::getLine() const
{
    auto x1 = ui->firstXDoubleSpinBox->value();
    auto y1 = ui->firstYDoubleSpinBox->value();

    auto x2 = ui->secondXDoubleSpinBox->value();
    auto y2 = ui->secondYDoubleSpinBox->value();

    auto first = Domain::Point(x1, y1);
    auto second = Domain::Point(x2, y2);

    return Domain::Line(first, second);
}

Domain::Spectre MainWindow::getSpectre() const
{
    auto center_x = ui->spectreCenterXDoubleSpinBox->value();
    auto center_y = ui->spectreCenterYDoubleSpinBox->value();
    auto angle = ui->spectreAngleDoubleSpinBox->value();
    auto len = ui->spectreLenDoubleSpinBox->value();
    return Domain::Spectre(Domain::Point(center_x, center_y), len, Helper::Math::degrees_to_radians(angle));
}

MainWindow::DrawAlgo MainWindow::getDrawAlgo() const
{
    return (MainWindow::DrawAlgo)ui->drawAlgoComboBox->currentIndex();
}

void MainWindow::on_undoAction_triggered()
{
    emit undo();
}

void MainWindow::on_backgroundColorPicked(const QColor &color)
{
    QString qss = QString("background-color: %1").arg(color.name());
    ui->graphicsView->setStyleSheet(qss);
}

void MainWindow::on_pickBackgroundColorPushButton_clicked()
{
    auto color_dialog = new QColorDialog(this);
    color_dialog->show();
    QObject::connect(color_dialog, &QColorDialog::colorSelected, this, &MainWindow::on_backgroundColorPicked);
}


void MainWindow::on_clearCanvasAction_triggered()
{
    emit clearCanvas();
}


void MainWindow::on_increaseScalePushButton_clicked()
{
    ui->graphicsView->scale(1.5, 1.5);
}


void MainWindow::on_dereaseScalePushButton_clicked()
{
    ui->graphicsView->scale(1 / 1.5, 1 / 1.5);
}


void MainWindow::on_authorAction_triggered()
{
    QMessageBox msgBox;
    msgBox.setText("Автор.");
    msgBox.setInformativeText("Булгаков Иван ИУ7-44Б.");
    msgBox.setDefaultButton(QMessageBox::Ok);
    msgBox.exec();
}

void MainWindow::on_timeAction_triggered()
{
    qreal len = 100;

    QStringList categories;
    categories << "Библиотечная" << "ЦДА" << "Брезенхэм (вещественные)" << "Брезенхэм (целые)" << "Брезенхэм со сглаживанием" << "Ву";

    auto sets = QList<QBarSet*>();
    for (int curType = 0; curType <= DrawAlgo::Wu; curType++)
    {
        sets.append(new QBarSet(categories[curType]));
    }

    auto fake_canvas = new QGraphicsView();
    fake_canvas->setScene(new QGraphicsScene());

    std::vector<double> timings(DrawAlgo::Wu + 1);

    int iteration_num = 1000;
    double angle = PI / 1000;
    for (int i = 0; i < 1000; ++i)
        for (int curType = 0; curType <= DrawAlgo::Wu; curType++)
        {
            auto p1 = Domain::Point(0, 0);
            auto p2 = Domain::Point(len, len);
            auto line = Domain::Line(p1, p2).Rotate(Domain::Point(len / 2, len / 2), angle);
            angle += angle;
            auto command = Domain::DrawLineCommand(line, Qt::black, fake_canvas, (DrawAlgo)curType);

            auto t1 = std::chrono::high_resolution_clock::now();
            command.execute();
            auto t2 = std::chrono::high_resolution_clock::now();

            std::chrono::duration<double, std::milli> ms_double = t2 - t1;
            timings[curType] += ms_double.count();
        }

    delete fake_canvas;

    for (int curType = 0; curType <= DrawAlgo::Wu; curType++)
    {
        sets[curType]->append(timings[curType]);
    }
    QBarSeries *series = new QBarSeries();
    series->append(sets);

    QChart *chart = new QChart();
    chart->addSeries(series);
    chart->setTitle("Временные характеристики алгоритмов (время за 1000 проходов)");
    chart->setAnimationOptions(QChart::SeriesAnimations);

    QValueAxis *axisY = new QValueAxis();
    axisY->setTickCount(20);
    axisY->setLabelFormat("%.ems");
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);

    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    QStringList methods;
    methods << QString("Длина %1").arg(len);
    axisX->append(methods);
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    chartView->resize(QSize(900, 600));
    chartView->show();
}


void MainWindow::on_gradationAction_triggered()
{
    qreal len = 100;
    int interval = 10;

    QStringList categories;
    categories << "ЦДА" << "Брезенхэм (вещественные)" << "Брезенхэм (целые)" << "Брезенхэм (устранение ступенчатости)" << "Ву";

    QList <QLineSeries *> sets = QList <QLineSeries *> ();
    for (int curType = 0; curType < categories.length(); curType++)
    {
        QLineSeries *series = new QLineSeries();
        series->setName(categories[curType]);
        sets.append(series);
    }

    for (int angle = 0; angle <= 90; angle += interval)
        for (int curType = 0; curType < categories.length(); curType++)
        {
            qreal rad = angle * PI / 180;

            auto start = Domain::Point(0, 0);
            auto end = Domain::Point(start.x() + cos(rad) * len, start.y() - sin(rad) * len);

            auto line = Domain::Line(start, end);
            int step = 0;
            switch (curType)
            {
            case 0:
                Delivery::PointsCDA(line, &step);
                break;
            case 1:
                Delivery::PointsBresenhamFloat(line, &step);
                break;
            case 2:
                Delivery::PointsBresehnamInteger(line, &step);
                break;
            case 3:
                Delivery::PointsBresehnamSmooth(line, Qt::black, &step);
                break;
            case 4:
                Delivery::PointsWu(line, Qt::black, &step);
                break;
            }
            sets[curType]->append(QPointF(angle, step));
        }

    QChart *chart = new QChart();

    for (int curType = 0; curType < categories.length(); curType++)
        chart->addSeries(sets[curType]);

    chart->setTitle("Ступенчатость отрезков");
    chart->setAnimationOptions(QChart::SeriesAnimations);
    chart->createDefaultAxes();

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    chartView->resize(QSize(900, 600));
    chartView->show();
}

