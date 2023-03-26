#include "math.h"

namespace Helper {

qreal Math::degrees_to_radians(qreal degrees)
{
    return degrees * PI / TO_RADIANS;
}

} // namespace Helper
