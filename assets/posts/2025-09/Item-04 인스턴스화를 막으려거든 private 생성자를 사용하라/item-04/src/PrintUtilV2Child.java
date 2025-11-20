public class PrintUtilV2Child extends PrintUtilV2 {

    public final String info = "PrintUtilV2Child";

    // 정적 메서드는 오버라이딩이(overriding) 아니라 하이딩(hiding)
    public static void print(String msg) {
        System.out.println(msg);
    }
}
