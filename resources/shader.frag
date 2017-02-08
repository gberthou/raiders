uniform sampler2D texture;
uniform float     aspectRatio;
uniform float     baseLuminance;

uniform vec2      allies[16];
uniform float     ranges[16];

const float ATTENUATION = .01;

float distanceScaleInsensitive(vec2 a, vec2 b)
{
    float dx = (a.x - b.x);
    float dy = (a.y - b.y) / aspectRatio;
    return sqrt(dx * dx + dy * dy);
}

float computeFactor(float x, float range)
{
    if(range <= 0.)
        return 0.;

    if(x <= range)
        return 1.;

    float a = -1. / (ATTENUATION * (2. * range + ATTENUATION));
    float c = 1. - a * range * range;
    return clamp(a * x * x + c, 0., 1.);
}

float computeLight(vec2 position)
{
    float ret = 0.;
    for(int i = 0; i < 16; ++i)
    {
        float d = distanceScaleInsensitive(position, allies[i]);
        ret += computeFactor(d, ranges[i]);
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

