uniform vec3 domainPositions[64];
uniform float domainCount;
uniform vec4 palette[8];

struct Result
{
    int index;
    float d;
};

Result closestDomainIndex(vec2 point)
{
    float minDistance = 1.5;
    int ret = 0;
    for(int i = 0; i < int(domainCount); ++i)
    {
        float d = distance(point, domainPositions[i].xy);
        if(d < minDistance)
        {
            minDistance = d;
            ret = i;
        }
    }
    return Result(ret, minDistance);
}

void main()
{
    Result result = closestDomainIndex(gl_TexCoord[0].xy);
    if(result.d < 0.005)
        gl_FragColor = vec4(0., 0., 0., 1.);
    else
        gl_FragColor = palette[int(domainPositions[result.index].z)];

}

