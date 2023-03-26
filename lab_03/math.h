#ifndef HELPER_MATH_H
#define HELPER_MATH_H

#define PI acos(-1)
#define TO_RADIANS 180

#include <QtMath>

namespace Helper {

class Math
{
public:
    Math() = delete;
    static qreal degrees_to_radians(qreal degrees);
};

} // namespace Helper

#endif // HELPER_MATH_H
