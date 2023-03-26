#ifndef DOMAIN_COMMAND_H
#define DOMAIN_COMMAND_H

#include "domain/line.h"
#include "delivery/line.h"
#include "spectre.h"

#include <QGraphicsView>

namespace Domain {

class Command
{
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class DrawLineCommand : public Command
{
private:
    QGraphicsView *canvas;
    QColor color;
    Delivery::Line *canvas_line;
public:
    DrawLineCommand(const Domain::Line &_line, const QColor &_color, QGraphicsView *_canvas);
    ~DrawLineCommand();
    void execute() override;
    void undo() override;
};

class DrawSpectreCommand : public Command
{
private:
    QGraphicsView *canvas;
    QColor color;
    std::vector<Delivery::Line*> canvas_lines;
public:
    DrawSpectreCommand(const Domain::Spectre &_spectre, const QColor &_color, QGraphicsView *_canvas);
    ~DrawSpectreCommand();
    void execute() override;
    void undo() override;
};

} // namespace Domain

#endif // DOMAIN_COMMAND_H
