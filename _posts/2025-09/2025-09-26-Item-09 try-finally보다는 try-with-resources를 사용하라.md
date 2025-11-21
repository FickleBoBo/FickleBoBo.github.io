---
title: "[Item-09] try-finally보다는 try-with-resources를 사용하라"
date: 2025-09-26
categories: [Java, Effective Java 3/E]
tags: [Effective Java 3/E]
toc: true
math: true
image: /assets/posts/2025-09/Item-09%20try-finally보다는%20try-with-resources를%20사용하라/thumbnail.jpg
---

## Intro

Java 라이브러리에는 close 메서드를 호출해 직접 닫아줘야 하는 자원이 많다. [java.io.InputStream](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/InputStream.html), [java.io.OutputStream](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/OutputStream.html), [java.sql.Connection](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Connection.html) 등이 좋은 예다. 자원 닫기는 클라이언트가 놓치기 쉬워서 예측할 수 없는 성능 문제로 이어지기도 한다. 이런 자원 중 상당수가 안전망으로 finalizer를 활용하고 있지만 finalizer는 그리 믿을만하지 못하다.(아이템 8)

전통적으로 자원이 제대로 닫힘을 보장하는 수단으로 try-finally가 쓰였다. 예외가 발생하거나 메서드에서 반환되는 경우를 포함해서 말이다.

---

## V0

먼저 테스트를 위해 `FileReader`, `FileWriter` 클래스를 상속 받아 자원 생성과 회수 부분에 출력 로직을 추가해줬다.

```java
// FileReader 클래스를 상속 받아 자원 생성, 회수 출력 로직만 추가
public class MyFileReader extends FileReader {

    public MyFileReader(String fileName) throws FileNotFoundException {
        super(fileName);
        System.out.println("FileReader 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("reader close() 호출 전");
        super.close();
        System.out.println("reader close() 호출 후");
    }
}
```

```java
// FileWriter 클래스를 상속 받아 자원 생성, 회수 출력 로직만 추가
public class MyFileWriter extends FileWriter {

    public MyFileWriter(String fileName) throws IOException {
        super(fileName);
        System.out.println("FileWriter 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("writer close() 호출 전");
        super.close();
        System.out.println("writer close() 호출 후");
    }
}
```

---

## V1

파일에서 첫 줄을 읽어 반환하는 간단한 메서드로 자원 반납 후 리턴하도록 구현되있다. 해당 메서드는 읽을 파일의 확장자가 .dat면 예외를 던지도록 되어있다.

```java
    static String firstLineOfFileV1(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        // .dat 확장자면 예외를 던짐
        if (path.endsWith(".dat")) {
            throw new IOException("firstLineOfFileV1 .dat 파일 확장자 예외");
        }

        String line = br.readLine();

        // 자원 회수
        br.close();

        return line;
    }
```

해당 메서드는 정상 동작할 경우 설계한대로 자원도 반납하고 결과도 잘 출력되지만 예외가 발생할 경우 close 메서드 호출에 실패하게 된다.

```java
        try {
            System.out.println(firstLineOfFileV1("resources/data.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // reader close() 호출 전
            // reader close() 호출 후
            // abc
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(firstLineOfFileV1("resources/data.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@4e50df2e
            // java.io.IOException: firstLineOfFileV1 .dat 파일 확장자 예외
            //     at TryFinallyV1.firstLineOfFileV1(TryFinallyV1.java:59)
            //     at TryFinallyV1.main(TryFinallyV1.java:20)
            // -> 예외가 터지며 자원 회수 실패
        }
```

예외가 터지거나 return 문을 만나면 메서드를 빠져나오므로 당연한 결과이다. 항상 자원의 반납을 보장하려면 try-finally 구문을 활용하면 된다.

```java
    static String firstLineOfFileV2(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        try {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("firstLineOfFileV2 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } finally {
            // 자원 회수
            br.close();
        }
    }
```

항상 finally 구문의 close 메서드가 잘 호출된다.

```java
        try {
            System.out.println(firstLineOfFileV2("resources/data.txt"));
            // FileReader 생성 = io.MyFileReader@6e8cf4c6
            // reader close() 호출 전
            // reader close() 호출 후
            // abc
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(firstLineOfFileV2("resources/data.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@12edcd21
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: firstLineOfFileV2 .dat 파일 확장자 예외
            //     at TryFinallyV1.firstLineOfFileV2(TryFinallyV1.java:76)
            //     at TryFinallyV1.main(TryFinallyV1.java:41)
            // -> 예외가 터졌지만 자원 회수 성공
        }
```

---

## V2

사용하는 자원이 여러 개면 try-finally 구문을 중첩해서 활용하면 된다.

```java
    // 중첩된 try-finally 블록으로 코드가 복잡해진다(자원의 생명주기도 고려해야 한다)
    static String copyV1(String src, String dst) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(src));

        try {
            BufferedWriter bw = new BufferedWriter(new MyFileWriter(dst));

            try {
                // .dat 확장자면 예외를 던짐
                if (src.endsWith(".dat")) {
                    throw new IOException("copyV1 .dat 파일 확장자 예외");
                }

                String line;
                while ((line = br.readLine()) != null) {
                    bw.write(line);
                }
                return "ok";
            } finally {
                bw.close();
            }
        } finally {
            br.close();
        }
    }
```

두 자원 모두 잘 반납된 것을 볼 수 있다.

```java
        try {
            System.out.println(copyV1("resources/data.txt", "resources/dataV1.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter@7291c18f
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // ok
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(copyV1("resources/data.dat", "resources/dataV1.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@7cc355be
            // FileWriter 생성 = io.MyFileWriter@6e8cf4c6
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV1 .dat 파일 확장자 예외
            //     at TryFinallyV2.copyV1(TryFinallyV2.java:70)
            //     at TryFinallyV2.main(TryFinallyV2.java:26)
            // -> 예외가 터졌지만 자원 회수 성공
        }
```

아래 메서드는 MyFileWriter2로 구현체를 바꾼 것으로 close 메서드에서 예외를 던지게 오버라이딩 했다.

```java
    static String copyV2(String src, String dst) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(src));

        try {
            BufferedWriter bw = new BufferedWriter(new MyFileWriter2(dst));

            try {
                // .dat 확장자면 예외를 던짐
                if (src.endsWith(".dat")) {
                    throw new IOException("copyV2 .dat 파일 확장자 예외");
                }

                String line;
                while ((line = br.readLine()) != null) {
                    bw.write(line);
                }
                return "ok";
            } finally {
                bw.close();
            }
        } finally {
            br.close();
        }
    }
```

```java
public class MyFileWriter2 extends FileWriter {

    public MyFileWriter2(String fileName) throws IOException {
        super(fileName);
        System.out.println("FileWriter 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("writer close() 호출 전2");
        throw new IOException("writer close 호출 중 예외 발생");
    }
}
```

아래처럼 .dat 확장자를 파라미터로 넘기면 파일 확장자에서 먼저 예외가 터지고 finally 블럭에서 writer를 close 할 때 또 예외가 터진다. 핵심 예외는 파일 확장자 예외인데 자원 반납 예외가 이를 덮어쓰게 된다.

```java
        try {
            System.out.println(copyV2("resources/data.dat", "resources/dataV2.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@27973e9b
            // FileWriter 생성 = io.MyFileWriter2@7530d0a
            // writer close() 호출 전2
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: writer close 호출 중 예외 발생
            //     at io.MyFileWriter2.close(MyFileWriter2.java:16)
            //     at java.base/java.io.BufferedWriter.implClose(BufferedWriter.java:398)
            //     at java.base/java.io.BufferedWriter.close(BufferedWriter.java:386)
            //     at TryFinallyV2.copyV2(TryFinallyV2.java:100)
            //     at TryFinallyV2.main(TryFinallyV2.java:42)
            // -> 예외는 finally 블럭에서도 발생할 수 있으며 핵심 예외인 파일 확장자 예외가 writer 자원 회수 실패 예외에 덮혀짐
        }
```

---

## V3

개발자의 실수, 자원의 생명주기를 고려한 복잡한 자원 반납, 핵심 예외 덮힘, finally 블록에서 자원 반납을 위해 try 블록 바깥에 변수 선언(변수 스코프가 넓어짐) 등 머리가 아픈데 이걸 깔끔하게 해결해주는게 try-with-resources 구문이다.

아래처럼 소괄호에 사용할 자원을 명시만 해주면 된다.

```java
    static String copyV3(String src, String dst) throws IOException {
        try (BufferedReader br = new BufferedReader(new MyFileReader(src));
             BufferedWriter bw = new BufferedWriter(new MyFileWriter(dst))) {

            // .dat 확장자면 예외를 던짐
            if (src.endsWith(".dat")) {
                throw new IOException("copyV3 .dat 파일 확장자 예외");
            }

            String line;
            while ((line = br.readLine()) != null) {
                bw.write(line);
            }
            return "ok";
        }
    }
```

출력 결과에서 볼 수 있듯이 try에서 명시한 순서의 역순으로 자원이 반납된다. 예외가 발생해도 자원 반납이 이루어지는 것을 볼 수 있다.

```java
        try {
            System.out.println(copyV3("resources/data.txt", "resources/dataV3.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter@7291c18f
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // ok
            // -> try-with-resources 구문에서 명시한 순서의 반대 순서로 닫아줌
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(copyV3("resources/data.dat", "resources/dataV3.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@7cc355be
            // FileWriter 생성 = io.MyFileWriter@6e8cf4c6
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV3 .dat 파일 확장자 예외
            //     at TryWithResourcesV1.copyV3(TryWithResourcesV1.java:70)
            //     at TryWithResourcesV1.main(TryWithResourcesV1.java:27)
            // -> 예외가 발생해서 자원 회수 잘함
        }
```

writer 구현체를 close 메서드에서 예외를 던지는 구현체로 바꾼 경우

```java
    static String copyV4(String src, String dst) throws IOException {
        try (BufferedReader br = new BufferedReader(new MyFileReader(src));
             BufferedWriter bw = new BufferedWriter(new MyFileWriter2(dst))) {

            // .dat 확장자면 예외를 던짐
            if (src.endsWith(".dat")) {
                throw new IOException("copyV4 .dat 파일 확장자 예외");
            }

            String line;
            while ((line = br.readLine()) != null) {
                bw.write(line);
            }
            return "ok";
        }
    }
```

아래처럼 핵심 예외가 먼저 표시되고 자원 반납 과정에서 던진 예외가 따라 나오는 것을 볼 수 있다.

```java
        try {
            System.out.println(copyV4("resources/data.dat", "resources/dataV4.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter2@7291c18f
            // writer close() 호출 전2
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV4 .dat 파일 확장자 예외
            //     at TryWithResourcesV1.copyV4(TryWithResourcesV1.java:87)
            //     at TryWithResourcesV1.main(TryWithResourcesV1.java:43)
            //     Suppressed: java.io.IOException: writer close 호출 중 예외 발생
            //         at io.MyFileWriter2.close(MyFileWriter2.java:16)
            //         at java.base/java.io.BufferedWriter.implClose(BufferedWriter.java:398)
            //         at java.base/java.io.BufferedWriter.close(BufferedWriter.java:386)
            //         at TryWithResourcesV1.copyV4(TryWithResourcesV1.java:82)
            //         ... 1 more
            // -> 핵심 예외인 파일 확장자 예외가 잘나옴
        }
```

---

## try-with-resources 추가 내용

Java7부터 이런 자원의 반납을 편하게 할 수 있는 try-with-resources 편의기능이 추가되었다.

위의 try-with-resources 구문을 보면 close 메서드를 호출하는 부분이 없는데 close 메서드가 알아서 호출되고 있다. 이는 명시한 자원이 [AutoCloseable](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/AutoCloseable.html) 인터페이스를 구현하고 있어서 가능한 것으로 try-with-resources 구문에 명시할 자원은 해당 인터페이스를 반드시 구현해야 한다.(MyFileReader -> FileReader -> InputStreamReader -> Reader -> Closeable -> AutoCloseable) 그러면 try 블럭이 끝나는 시점에 close 메서드를 호출하여 자원을 반납해준다.

이처럼 try-with-resources를 활용하면 실수로 자원을 반납하지 않는 문제를 방지할 수 있고, 코드의 간결성 및 가독성이 향상된다. catch 구문까지 활용하는 경우 try-catch-finally 구문은 catch 이후 finally가 실행되는데 try-with-resources는 자원을 먼저 반납하고 예외 처리가 돼서 자원 반납이 약간 더 빠르다는 장점도 있다.

```java
public class TryWithResourcesV2 {

    public static void main(String[] args) throws IOException {
        System.out.println(testV1("resources/data.dat"));
        // FileReader 생성 = io.MyFileReader@10f87f48
        // catch 블럭
        // reader close() 호출 전
        // reader close() 호출 후
        // testV1 .dat 파일 확장자 예외
        // -> catch 블럭 수행 후 finally 블럭에서 자원 반납
        System.out.println(testV2("resources/data.dat"));

        // FileReader 생성 = io.MyFileReader@10f87f48
        // reader close() 호출 전
        // reader close() 호출 후
        // catch 블럭
        // testV2 .dat 파일 확장자 예외
        // -> close 메서드를 먼저 호출하고 catch 블럭 수행
    }

    static String testV1(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        try {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("testV1 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } catch (IOException e) {
            System.out.println("catch 블럭");
            return e.getMessage();
        } finally {
            // 자원 회수
            br.close();
        }
    }

    static String testV2(String path) {
        try (BufferedReader br = new BufferedReader(new MyFileReader(path))) {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("testV2 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } catch (IOException e) {
            System.out.println("catch 블럭");
            return e.getMessage();
        }
    }
}
```

---
