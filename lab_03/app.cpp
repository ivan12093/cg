#include "app.h"
#include "domain/command.h"
#include "ui_mainwindow.h"
#include "mainwindow.h"

#include <iostream>

App::App(MainWindow *mw) : main_window(mw), command_stack()
{
    QObject::connect(main_window, &MainWindow::drawLineRequested, this, &App::on_drawLineRequest);
    QObject::connect(main_window, &MainWindow::drawSpectreRequested, this, &App::on_drawSpectreRequest);
    QObject::connect(main_window, &MainWindow::undo, this, &App::on_undo);
    QObject::connect(main_window, &MainWindow::clearCanvas, this, &App::on_clearCanvas);
}

App::~App()
{
    while (!command_stack.empty())
    {
        auto command = command_stack.top();
        command_stack.pop();
        delete command;
    }
}

void App::on_undo()
{
    if (command_stack.empty())
    {
        return;
    }
    auto command = command_stack.top();
    command->undo();
    command_stack.pop();
    delete command;
}

void App::on_clearCanvas()
{
    auto ui = main_window->getUi();
    auto clear_canvas_command = new Domain::ClearCanvasCommand(ui->graphicsView);

    clear_canvas_command->execute();
    command_stack.push(clear_canvas_command);
}

void App::on_drawLineRequest()
{
    auto line = main_window->getLine();
    auto pen_color = main_window->getPenColor();

    auto ui = main_window->getUi();
    auto draw_line_command = new Domain::DrawLineCommand(line, pen_color, ui->graphicsView);
    draw_line_command->execute();
    command_stack.push(draw_line_command);
}

void App::on_drawSpectreRequest()
{
    auto spectre = main_window->getSpectre();
    auto pen_color = main_window->getPenColor();

    auto ui = main_window->getUi();
    auto draw_spectre_command = new Domain::DrawSpectreCommand(spectre, pen_color, ui->graphicsView);
    draw_spectre_command->execute();
    command_stack.push(draw_spectre_command);
}
