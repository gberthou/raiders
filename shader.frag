uniform sampler2D texture;

uniform vec2      allies[16];
uniform float     ranges[16];

const float ATTENUATION = .01;

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
        float d = distance(position, allies[i]);
        ret += computeFactor(d, ranges[i]);
    }

    return clamp(ret, 0., 1.);
}

void main()
{
    // lookup the pixel in the texture
    vec3 pixel = vec3(texture2D(texture, gl_TexCoord[0].xy));

    // multiply it by the color
    gl_FragColor = vec4(pixel * computeLight(gl_TexCoord[0].xy), 1);
}

