uniform vec3 domainPositions[64];
uniform float domainCount;
uniform vec4 palette[8];

struct Result
{
    int index;
    float d;
    float factor;
};

float sigmoid(float x)
{
    float tmp = 1. - 1. / (1. + exp(-500. * (x - 0.98)));
    return tmp * 0.15 + 0.85;
}

Result closestDomainIndex(vec2 point)
{
    float minDistance = 1.5;
    float secondDistance = 1000.;
    int ret = 0;
    for(int i = 0; i < int(domainCount); ++i)
    {
        float d = distance(point, domainPositions[i].xy);
        if(d < minDistance)
        {
            secondDistance = minDistance;
            minDistance = d;
            ret = i;
        }
        else if(d < secondDistance)
            secondDistance = d;
    }

    return Result(ret, minDistance, sigmoid(minDistance / secondDistance));
}

void main()
{
    Result result = closestDomainIndex(gl_TexCoord[0].xy);
    if(result.d < 0.005)
        gl_FragColor = vec4(0., 0., 0., 1.);
    else
        gl_FragColor = vec4(result.factor * palette[int(domainPositions[result.index].z)].xyz, 1.);

}

