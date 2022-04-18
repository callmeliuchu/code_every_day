#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.14159265359
#define TWO_PI 6.28318530718


uniform vec2 u_resolution;

void main(){
    vec2 st = gl_FragCoord.xy / u_resolution;
    st.x *= u_resolution.x / u_resolution.y;
    st = st - 0.5;
    float a = atan(st.y,st.x);
    int N =  4;
    float alpha = TWO_PI / float(N);
    float d = length(st);
    if(a < 0.){
        a = a + TWO_PI;
    }
    float theta = a / alpha;
    theta = (theta - floor(theta))*alpha;
    float aa = (PI-alpha)/2.0;
    float beta = PI - theta - aa;
    float x = sin(aa)*0.4/sin(beta);
    gl_FragColor = vec4(vec3(step(x,d)),1.0);
}