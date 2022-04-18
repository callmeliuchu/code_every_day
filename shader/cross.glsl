#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;

float box(vec2 st,vec2 size){
    size = vec2(0.5) - size * 0.5;
    vec2 s1 = step(size,st);
    vec2 s2 = step(size,1.0-st);
    return s1.x * s2.x * s1.y * s2.y;
}

float cross(vec2 st,float size){
    return box(st,vec2(size,size/4.0)) + box(st,vec2(size/4.0,size));
}



void main(){
    vec2 st = gl_FragCoord.xy/u_resolution;
    st.x *= u_resolution.x / u_resolution.y;
    vec2 t = vec2(sin(2.0*u_time),cos(u_time));
    st += 0.35*t;
    float pct = cross(st,0.25);
    gl_FragColor = vec4(vec3(pct),1.0);
}