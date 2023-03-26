#include "line.h"
#include <QtMath>

namespace Domain {

Line::Line(const Point &_first, const Point &_second) : QLineF(_first, _second),
    first(_first), second(_second) {}

Line Line::Rotate(Point center, qreal angle)
{
    auto begin = first.Rotate(center, angle);
    auto end = second.Rotate(center, angle);

    return Line(begin, end);
}

} // namespace Domain
