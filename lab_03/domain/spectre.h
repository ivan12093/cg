#ifndef DOMAIN_SPECTRE_H
#define DOMAIN_SPECTRE_H

#include <vector>

#include "domain/point.h"
#include "domain/line.h"

namespace Domain {

class Spectre
{
private:
    Point center;
    qreal len;
    qreal angle;
public:
    Spectre(Point _center, qreal _len, qreal _angle);
    std::vector<Line> getLines() const;
};

} // namespace Domain

#endif // DOMAIN_SPECTRE_H
