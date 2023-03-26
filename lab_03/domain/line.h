#ifndef DOMAIN_LINE_H
#define DOMAIN_LINE_H

#include "point.h"
#include <QLineF>

namespace Domain {

class Line : public QLineF
{
private:
    Point first;
    Point second;
public:
    Line(const Point &_first, const Point &_second);
    Line Rotate(Point center, qreal angle);
};

} // namespace Domain

#endif // DOMAIN_LINE_H
