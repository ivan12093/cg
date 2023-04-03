#include "line.h"

#include <QPen>
#include <QPainter>

template<class T>
static int sign(T num)
{
    if (num > 0)
        return 1;
    if (num < 0)
        return -1;
    return 0;
}

namespace Delivery {

Line::Line(const Domain::Line &_line, const QColor &_color, DrawMethod method) :
    QGraphicsLineItem(_line), line(_line), draw_method(method)
{
    pen = QColor(_color);
    pen.setJoinStyle(Qt::MiterJoin);
    setPen(pen);
}

void Line::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    (this->*(draw_method))(painter, option, widget);
}

void Line::DrawDefault(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    painter->setPen(pen);
    QGraphicsLineItem::paint(painter, option, widget);
}

void Line::DrawCDA(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    auto points = PointsCDA(line);
    painter->setPen(pen);
    for (auto point: points)
    {
        painter->drawPoint(point);
    }
}

void Line::DrawBresehnamInteger(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    auto points = PointsBresehnamInteger(line);
    painter->setPen(pen);
    for (const QPoint &point: points)
    {
        painter->drawPoint(point);
    }
}

void Line::DrawBresenhamFloat(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    auto points = PointsBresenhamFloat(line);
    painter->setPen(pen);
    for (const QPoint &point: points)
    {
        painter->drawPoint(point);
    }
}

void Line::DrawBresehnamSmooth(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    auto points = PointsBresehnamSmooth(line, pen.color());

    for (const std::pair<QPoint, QColor> &pair : points)
    {
        painter->setPen(pair.second);
        painter->drawPoint(pair.first);
    }
}

void Line::DrawWu(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    auto points = PointsWu(line, pen.color());

    for (const std::pair<QPoint, QColor> pair : points)
    {
        painter->setPen(pair.second);
        painter->drawPoint(pair.first);
    }
}

std::vector<QPoint> PointsCDA(const Domain::Line &line, int *step)
{
    *step = 0;
    if (line.isNull())
    {
        return {line.p1().toPoint()};
    }

    auto cur_x = line.p1().x();
    auto cur_y = line.p1().y();

    auto dx = line.dx();
    auto dy = line.dy();

    int npoints = abs(dy);
    if (abs(dx) >= abs(dy))
    {
        npoints = abs(dx);
    }

    dx /= npoints;
    dy /= npoints;

    std::vector<QPoint> result(npoints + 2);
    for (int i = 0; i < npoints + 1; ++i)
    {
        result[i] = QPoint(qRound(cur_x), qRound(cur_y));
        cur_x += dx;
        cur_y += dy;

        if (step && !((qRound(cur_x + dx) == qRound(cur_x) && qRound(cur_y + dy) != qRound(cur_y)) ||
                      (qRound(cur_x + dx) != qRound(cur_x) && qRound(cur_y + dy) == qRound(cur_y))))
        {
            ++(*step);
        }
    }
    return result;
}

std::vector<QPoint> PointsBresehnamInteger(const Domain::Line &line, int *step)
{
    *step = 0;
    int dx = sign(line.dx());
    int dy = sign(line.dy());

    int lenX = abs(line.dx());
    int lenY = abs(line.dy());

    int len = std::max(lenX, lenY);

    if (len == 0)
    {
        return {line.p1().toPoint()};
    }

    std::vector<QPoint> result(len + 1);

    if (lenY <= lenX)
    {
        int x = line.p1().x();
        int y = line.p1().y();
        int d = -lenX;

        ++len;
        int i = 0;
        while (len--)
        {
            if (i > 0)
            {
                if (result[i - 1].x() != x && result[i - 1].y() != y)
                {
                    ++(*step);
                }
            }
            result[i] = QPoint(x, y);
            ++i;
            x += dx;
            d += 2 * lenY;
            if (d > 0)
            {
                d -= 2 * lenX;
                y += dy;
            }
        }
    }
    else
    {
        int x = line.p1().x();
        int y = line.p1().y();
        int d = -lenY;

        ++len;
        int i = 0;
        while (len--)
        {
            if (i > 0)
            {
                if (result[i - 1].x() != x && result[i - 1].y() != y)
                {
                    ++(*step);
                }
            }
            result[i] = QPoint(x, y);
            ++i;
            y += dy;
            d += 2 * lenX;
            if (d > 0)
            {
                d -= 2 * lenY;
                x += dx;
            }
        }
    }
    return result;
}

std::vector<QPoint> PointsBresenhamFloat(const Domain::Line &line, int *step)
{
    *step = 0;
    if (line.isNull())
    {
        return {line.p1().toPoint()};
    }

    auto x = line.x1();
    auto y = line.y1();

    auto dx = abs(line.dx());
    auto dy = abs(line.dy());

    auto sx = sign(line.dx());
    auto sy = sign(line.dy());

    bool swapped = false;
    if (dy > dx)
    {
        std::swap(dx, dy);
        swapped = true;
    }

    auto m = dy / dx;
    auto e = m - 0.5;
    int l = dx + 1;

    std::vector<QPoint> result(l);
    for (int i = 0; i < l; ++i)
    {
        if (i > 0 && step && !((result[i - 1].x() == x && result[i - 1].y() != y) ||
                               (result[i - 1].x() != x && result[i - 1].y() == y)))
        {
            ++(*step);
        }
        result[i] = QPoint(x, y);
        if (e >= 0)
        {
            if (swapped)
            {
                x += sx;
            }
            else
            {
                y += sy;
            }
            --e;
        }
        if (!swapped)
        {
            x += sx;
        }
        else
        {
            y += sy;
        }
        e += m;
    }
    return result;
}

static QColor choose_color(const QColor &color, int intensivity)
{
    QColor result = QColor(color);
    intensivity = std::min(intensivity, 255);
    intensivity = std::max(intensivity, 0);

    result.setAlpha(intensivity);
    return result;
}

std::vector<std::pair<QPoint, QColor>> PointsBresehnamSmooth(const Domain::Line &line,
                                                             const QColor &color, int *step)
{
    if (line.isNull())
    {
        return {{line.p1().toPoint(), color}};
    }

    int imax = 255;
    auto cur_x = line.x1();
    auto cur_y = line.y1();

    auto dx = line.dx();
    auto dy = line.dy();

    auto sx = sign(dx);
    auto sy = sign(dy);

    dx = abs(dx);
    dy = abs(dy);

    bool change = false;
    if (dy > dx)
    {
        change = true;
        std::swap(dx, dy);
    }

    auto m = dy / dx * imax;
    auto e = imax / 2.0;
    auto w = imax - m;
    auto l = qRound(dx) + 1;

    std::vector<std::pair<QPoint, QColor>> result(l);
    auto prev_x = cur_x;
    auto prev_y = cur_y;
    for (std::pair<QPoint, QColor> &pair: result)
    {
        if (step && !((prev_x == cur_x && prev_y != cur_y) || (prev_x != cur_x && prev_y == cur_y)))
        {
            ++(*step);
        }
        pair.first = QPoint(cur_x, cur_y);
        pair.second = choose_color(color, qRound(e));
        prev_x = cur_x;
        prev_y = cur_y;
        if (e <= w)
        {
            if (change)
            {
                cur_y += sy;
            }
            else
            {
                cur_x += sx;
            }
            e += m;
        }
        else
        {
            cur_x += sx;
            cur_y += sy;
            e -= w;
        }
    }
    return result;
}

std::vector<std::pair<QPoint, QColor>> PointsWu(const Domain::Line &line, const QColor &color, int *step)
{
    if (line.isNull())
    {
        return {{line.p1().toPoint(), color}};
    }

    int imax = 255;

    auto x0 = line.p1().x(), y0 = line.p1().y();
    auto x1 = line.p2().x(), y1 = line.p2().y();

    auto dx = line.dx();
    auto dy = line.dy();

    bool change = abs(dx) < abs(dy);
    if (change)
    {
        std::swap(x0, y0);
        std::swap(x1, y1);
    }
    if (x1 < x0)
    {
        std::swap(x0, x1);
        std::swap(y0, y1);
    }
    dx = x1 - x0;
    dy = y1 - y0;
    auto grad = dx ? dy / dx : 1;
    auto cur_y = y0;
    auto cur_x = x0;
    int l = 2 * (x1 - x0 + 1);
    auto prev_x = cur_x;
    auto prev_y = cur_y;
    std::vector<std::pair<QPoint, QColor>> result(l);
    for (int i = 0; i < l - 1; i += 2)
    {
        if (step && cur_x < line.x2())
        {
            if ((int)cur_y != (int)(cur_y + grad))
            {
                ++(*step);
            }
        }
        auto s = sign(cur_y);
        auto r1 = cur_y - (int)cur_y;
        auto r2 = 1 - r1;

        if (change)
        {
            result[i].second = choose_color(color, imax * r2);
            result[i].first = QPoint(cur_y, cur_x);
            result[i + 1].second = choose_color(color, imax * r1);
            result[i].first = QPoint(cur_y + s, cur_x);
        }
        else
        {
            result[i].second = choose_color(color, imax * r2);
            result[i].first = QPoint(cur_x, cur_y);
            result[i + 1].second = choose_color(color, imax * r1);
            result[i + 1].first = QPoint(cur_x, cur_y + s);
        }
        prev_x = cur_x;
        prev_y = cur_y;
        cur_y += grad;
        cur_x += 1;
    }
    return result;
}

} // namespace Delivery
