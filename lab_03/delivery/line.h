#ifndef DELIVERY_LINE_H
#define DELIVERY_LINE_H

#include "domain/line.h"

#include <QGraphicsLineItem>
#include <QPen>

namespace Delivery {

std::vector<QPoint> PointsCDA(const Domain::Line &line);
std::vector<QPoint> PointsBresehnamInteger(const Domain::Line &line);
std::vector<QPoint> PointsBresenhamFloat(const Domain::Line &line);
std::vector<std::pair<QPoint, QColor>> PointsBresehnamSmooth(const Domain::Line &line, const QColor &color);
std::vector<std::pair<QPoint, QColor>> PointsWu(const Domain::Line &line, const QColor &color);

class Line : public QGraphicsLineItem
{
public:
    using DrawMethod = void (Line::*)(QPainter*, const QStyleOptionGraphicsItem*, QWidget*);
private:
    QPen pen;
    Domain::Line line;
    DrawMethod draw_method;
public:
    Line(const Domain::Line &_line, const QColor &_color, DrawMethod method);
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget);
    void DrawDefault(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
    void DrawCDA(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
    void DrawBresehnamInteger(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
    void DrawBresenhamFloat(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
    void DrawBresehnamSmooth(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
    void DrawWu(QPainter *painter, const QStyleOptionGraphicsItem *option,
             QWidget *widget);
};

} // namespace Delivery

#endif // DELIVERY_LINE_H
