#include "line.h"

#include <QPen>

namespace Delivery {

Line::Line(const Domain::Line &_line, const QColor &_color) : QGraphicsLineItem(_line), color(_color)
{
    setPen(QPen(color));
}

} // namespace Delivery
