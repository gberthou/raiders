uniform sampler2D texture;

uniform vec2      allies[16];
uniform float     ranges[16];

float computeLight(vec2 position)
{
    float ret = 0.;
    for(int i = 0; i < 16; ++i)
    {
        float d = distance(position, allies[i]);
        if(d < ranges[i])
            ret += 1.;
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

