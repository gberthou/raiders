uniform sampler2D current;

void main()
{
    // lookup the pixel in the texture
    vec3 pixel = vec3(texture2D(current, gl_TexCoord[0].xy));

    // multiply it by the color
    gl_FragColor = vec4(pixel*.5, 1);
}

