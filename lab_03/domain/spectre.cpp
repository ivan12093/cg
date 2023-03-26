#include "spectre.h"
#include "math.h"

#include <iostream>

namespace Domain {

Spectre::Spectre(Point _center, qreal _len, qreal _angle) : center(_center), len(_len), angle(_angle) {}

std::vector<Line> Spectre::getLines() const
{
    Point begin = Point(center.x() - len / 2, center.y());
    Point end = Point(center.x() + len / 2, center.y());

    auto line = Line(begin, end);
    std::vector<Line> result;
    qreal total_angle = 0;

    while (fabs(total_angle) < 2 * PI)
    {
        result.push_back(line);
        line = line.Rotate(center, angle);
        total_angle += angle;
    }
    for (auto a : result)
        std::cerr << a.p1().x() << " " << a.p1().y() << "\n";

    return result;
}

} // namespace Domain