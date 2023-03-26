#include "command.h"
#include "delivery/line.h"

#include <iostream>

namespace Domain {

DrawLineCommand::DrawLineCommand(const Domain::Line &_line, const QColor &_color, QGraphicsView *_canvas) :
    canvas(_canvas), color(_color), canvas_line(nullptr)
{
    canvas_line = new Delivery::Line(_line, color);
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

DrawSpectreCommand::DrawSpectreCommand(const Spectre &_spectre, const QColor &_color, QGraphicsView *_canvas) :
    canvas(_canvas), color(_color), canvas_lines()
{
    auto lines = _spectre.getLines();
    canvas_lines.reserve(lines.size());
    for (const Domain::Line &line : lines)
    {
        auto canvas_line = new Delivery::Line(line, color);
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

} // namespace Domain
