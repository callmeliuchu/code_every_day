#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;

void main(){
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    st = st*2.0 - 1.0;
    st = abs(st);
    float dist = length(st - vec2(0.3));
    vec3 color = vec3(fract(dist*10.0));
    gl_FragColor = vec4(color,1.0);
}