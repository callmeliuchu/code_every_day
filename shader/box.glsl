#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;


void main(){
    vec2 st = gl_FragCoord.xy / u_resolution;
    st.x *= u_resolution.x / u_resolution.y;
    st = 10.0*st;
    st = fract(st);
    vec2 st1 = step(0.1,st);
    vec2 st2 = step(0.1,1.0-st);
    gl_FragColor = vec4(vec3(st1.x*st1.y*st2.x*st2.y),1.0);
}