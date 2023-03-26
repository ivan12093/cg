#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "domain/line.h"
#include "math.h"

#include <iostream>
#include <QPalette>
#include <QColorDialog>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , pen_color(Qt::black)
{
    ui->setupUi(this);

    // connect signals
    QObject::connect(ui->drawLinePushButton, &QAbstractButton::clicked, this, &MainWindow::drawLineRequested);
    QObject::connect(ui->drawSpectrePushButton, &QAbstractButton::clicked, this, &MainWindow::drawSpectreRequested);

    QObject::connect(ui->graphicsView, &QGraphicsScene::wheelEvent)

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

QString MainWindow::getDrawAlgo() const
{
    return ui->drawAlgoComboBox->currentText();
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

