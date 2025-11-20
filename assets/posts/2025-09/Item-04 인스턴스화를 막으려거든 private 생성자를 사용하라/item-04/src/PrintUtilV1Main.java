public class PrintUtilV1Main {

    public static void main(String[] args) {
        PrintUtilV1.print("hello java V1");  // hello java V1

        /*
         * 생성자를 명시하지 않으면 컴파일러가 자동으로 기본 생성자를 만들어 준다.
         * 유틸리티 클래스를 인스턴스화해서 사용하는 것은 원하는 사용 방식이 아니다.
         * 인텔리제이가 경고도 해줌(Instantiation of utility class 'PrintUtilV1')
         */
        PrintUtilV1 p1 = new PrintUtilV1();
    }
}
