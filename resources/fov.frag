uniform sampler2D texture;
uniform float     aspectRatio;
uniform float     baseLuminance;

uniform vec2      allies[16];
uniform float     ranges[16];

uniform vec4      edges[2048];

const float ATTENUATION = .01;

float cross2(vec2 a, vec2 b)
{
    return a.x*b.y - a.y*b.x;
}

bool segmentsIntersect(int edgeOffset, vec2 a, vec2 b)
{
    vec4 tmp = edges[edgeOffset];
    vec2 edge = tmp.zw - tmp.xy;
    vec2 v    = b - a;
    float p = cross2(edge, v);
    vec2 CA = a - tmp.xy;
    float t = cross2(CA, v) / p;
    float u = cross2(CA, edge) / p;
    return t >= 0. && t <= 1. && u >= 0. && u <= 1.;
}

float distanceScaleInsensitive2(vec2 a, vec2 b)
{
    float dx = (a.x - b.x);
    float dy = (a.y - b.y) / aspectRatio;
    return dx * dx + dy * dy;
}

float computeFactor(float x2, float range)
{
    if(range <= 0.)
        return 0.;

    float range2 = range * range;

    if(x2 <= range2)
        return 1.;

    float a = -1. / (ATTENUATION * (2. * range + ATTENUATION));
    float c = 1. - a * range2;
    return clamp(a * x2 + c, 0., 1.);
}

float computeLight(vec2 position)
{
    float ret = 0.;
    for(int i = 0; i < 16; ++i)
    {
        if(ranges[i] == 0.)
            continue;

        float d2 = distanceScaleInsensitive2(position, allies[i]);
        /* Optimization: if distance >= 110% of range, do not waste time on
         * computing segment intersections, light contribution is 0
         */
        if(d2 >= ranges[i]*ranges[i]*1.21)
            continue;       

        bool hidden = false;
        for(int j = 0; j < 2048 && !hidden && edges[j] != vec4(0, 0, 0, 0); ++j)
            hidden = segmentsIntersect(j, position, allies[i]);

        if(!hidden)
            ret += computeFactor(d2, ranges[i]);
    }

    return clamp(ret, baseLuminance, 1.);
}

void main()
{
    // lookup the pixel in the texture
    vec3 pixel = vec3(texture2D(texture, gl_TexCoord[0].xy));

    // multiply it by the color
    gl_FragColor = vec4(pixel * computeLight(gl_TexCoord[0].xy), 1);
}

