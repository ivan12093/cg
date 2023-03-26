#include "point.h"

namespace Domain {

Point::Point(qreal x, qreal y) : QPointF(x, y) {}

Point Point::Rotate(Point center, qreal angle)
{
    qreal new_x = center.x() + (x() - center.x()) * cos(angle) - (y() - center.y()) * sin(angle);
    qreal new_y = center.x() + (x() - center.x()) * sin(angle) + (y() - center.y()) * cos(angle);

    return Point(new_x, new_y);
}

} // namespace Domain
