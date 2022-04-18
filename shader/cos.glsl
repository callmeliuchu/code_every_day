#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;

void main(){
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    st = st - vec2(0.5);
    float r = length(st);
    float a = atan(st.y,st.x);
    vec3 color = vec3(step(r*4.0,cos(a*3.0)));
    gl_FragColor = vec4(color,1.0);

}