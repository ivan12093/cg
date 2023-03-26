#ifndef DOMAIN_POINT_H
#define DOMAIN_POINT_H

#include <QPointF>

namespace Domain {

class Point : public QPointF
{
public:
    Point(qreal x, qreal y);
    Point Rotate(Point center, qreal angle);
};

} // namespace Domain
#endif // DOMAIN_POINT_H
