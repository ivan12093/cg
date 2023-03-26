#ifndef DELIVERY_LINE_H
#define DELIVERY_LINE_H

#include "domain/line.h"

#include <QGraphicsLineItem>

namespace Delivery {

class Line : public QGraphicsLineItem
{
private:
    QColor color;
public:
    Line(const Domain::Line &_line, const QColor &_color);
};

} // namespace Delivery

#endif // DELIVERY_LINE_H
