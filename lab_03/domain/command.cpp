#include "command.h"
#include "delivery/line.h"

#include <iostream>

static Delivery::Line::DrawMethod get_method_by_name(MainWindow::DrawAlgo algo)
{
    Delivery::Line::DrawMethod result = &Delivery::Line::DrawDefault;
    switch (algo) {
    case MainWindow::DrawAlgo::Default:
        result = &Delivery::Line::DrawDefault;
        break;
    case MainWindow::DrawAlgo::CDA:
        result = &Delivery::Line::DrawCDA;
        break;
    case MainWindow::DrawAlgo::BresenhamInteger:
        result = &Delivery::Line::DrawBresehnamInteger;
        break;
    case MainWindow::DrawAlgo::BresenhamFloat:
        result = &Delivery::Line::DrawBresenhamFloat;
        break;
    case MainWindow::DrawAlgo::BresenhamSmooth:
        result = &Delivery::Line::DrawBresehnamSmooth;
        break;
    case MainWindow::DrawAlgo::Wu:
        result = &Delivery::Line::DrawWu;
        break;
    default:
        break;
    }
    return result;
}

namespace Domain {

DrawLineCommand::DrawLineCommand(const Domain::Line &_line, const QColor &_color, QGraphicsView *_canvas,
                                 MainWindow::DrawAlgo _algo) :
    canvas(_canvas), color(_color), canvas_line(nullptr)
{
    algo = get_method_by_name(_algo);
    canvas_line = new Delivery::Line(_line, color, algo);
}

DrawLineCommand::~DrawLineCommand()
{
    delete canvas_line;
}

void DrawLineCommand::execute()
{
    canvas->scene()->addItem(canvas_line);
}

void DrawLineCommand::undo()
{
    canvas->scene()->removeItem(canvas_line);
}

DrawSpectreCommand::DrawSpectreCommand(const Spectre &_spectre, const QColor &_color, QGraphicsView *_canvas,
                                       MainWindow::DrawAlgo _algo) :
    canvas(_canvas), color(_color), canvas_lines()
{
    algo = get_method_by_name(_algo);
    auto lines = _spectre.getLines();
    canvas_lines.reserve(lines.size());
    for (const Domain::Line &line : lines)
    {
        auto canvas_line = new Delivery::Line(line, color, algo);
        canvas_lines.push_back(canvas_line);
    }
}

DrawSpectreCommand::~DrawSpectreCommand()
{
    for (auto ptr : canvas_lines)
    {
        delete ptr;
    }
}

void DrawSpectreCommand::execute()
{
    for (auto canvas_line : canvas_lines)
    {
        canvas->scene()->addItem(canvas_line);
    }
}

void DrawSpectreCommand::undo()
{
    for (auto canvas_line : canvas_lines)
    {
        canvas->scene()->removeItem(canvas_line);
    }
}

ClearCanvasCommand::ClearCanvasCommand(QGraphicsView *_canvas) : canvas(_canvas), deleted() {}

void ClearCanvasCommand::execute()
{
    deleted = canvas->scene()->items();
    for (auto to_delete : deleted)
    {
        canvas->scene()->removeItem(to_delete);
    }
}

void ClearCanvasCommand::undo()
{
    for (auto to_add : deleted)
    {
        canvas->scene()->addItem(to_add);
    }
}

} // namespace Domain
