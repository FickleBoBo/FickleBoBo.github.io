---
title: "[Item-35] ordinal 메서드 대신 인스턴스 필드를 사용하라"
date: 2025-10-24
categories: [Book, Effective Java 3/E]
tags: [Effective Java 3/E]
toc: true
math: true
image: /assets/posts/2025-10/Item-35%20ordinal%20메서드%20대신%20인스턴스%20필드를%20사용하라/thumbnail.jpg
---

## ordinal 메서드 활용 예시

[ordinal](<https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Enum.html#ordinal()>) 메서드는 열거 타입의 상수들에 대해 열거 타입에서 몇 번째 위치인지 반환하는 메서드이다.(첫번째 위치 = 0, 두번째 위치 = 1, ...) 이런 특징을 활용하면 마치 인덱스를 부여하듯 여러가지 활용 방안이 떠오를 수 있지만 이는 유지보수에 재앙이다.

아래는 합주단의 종류를 나열한 열거 타입으로 SOLO는 1명, DUET은 2명 이렇게 선형 증가하므로 ordinal 메서드를 적용하면 합주단의 인원수를 간단하게 반환할 수 있다.

```java
public enum Ensemble {
    SOLO, DUET, TRIO, QUARTET, QUINTET,
    SEXTET, SEPTET, OCTET, NONET, DECTET;

    public int numberOfMusicians() {
        return ordinal() + 1;
    }
}
```

```java
    public static void main(String[] args) {
        for (Ensemble e : Ensemble.values()) {
            System.out.println(e + " = " + e.numberOfMusicians());
            // 출력 결과
            // SOLO = 1
            // DUET = 2
            // TRIO = 3
            // QUARTET = 4
            // QUINTET = 5
            // SEXTET = 6
            // SEPTET = 7
            // OCTET = 8
            // NONET = 9
            // DECTET = 10
        }
    }
```

이런 코드는 잘 동작은 하지만 유지보수에 끔찍한 코드다. 상수의 선언 순서가 바뀔 경우 오작동하며, 동일한 수를 추가할 방법도 없다. 얘를 들면 `OCTET(8중주)` 상수가 있으니 똑같이 8명이 연주하는 `DOUBLE_QUARTET(복4중주)`를 추가할 수 없다. 중간에 한 자리가 빌 경우 수를 유지하지 위해 의미없는 상수를 추가해야할 수도 있다.

해결책은 간단하다. ordinal 메서드를 사용하지 말고 필요한 값은 인스턴스 필드로 저장하자.

```java
public enum Ensemble {
    SOLO(1), DUET(2), TRIO(3), QUARTET(4),
    QUINTET(5), SEXTET(7), SEPTET(7), OCTET(8), DOUBLE_QUARTET(8),
    NONET(9), DECTET(10), TRIPLE_QUARTET(12);

    private final int numberOfMusicians;

    Ensemble(int numberOfMusicians) {
        this.numberOfMusicians = numberOfMusicians;
    }

    public int numberOfMusicians() {
        return numberOfMusicians;
    }
}
```

```java
    public static void main(String[] args) {
        for (Ensemble e : Ensemble.values()) {
            System.out.println(e + " = " + e.numberOfMusicians());
            // 출력 결과
            // SOLO = 1
            // DUET = 2
            // TRIO = 3
            // QUARTET = 4
            // QUINTET = 5
            // SEXTET = 7
            // SEPTET = 7
            // OCTET = 8
            // DOUBLE_QUARTET = 8
            // NONET = 9
            // DECTET = 10
            // TRIPLE_QUARTET = 12
        }
    }
```

위처럼 인스턴스 필드에 합주단의 인원수를 추가함으로서 똑같이 8명이 연주하는 `DOUBLE_QUARTET(복4중주)`를 추가할 수 있었고, 12명이 연주하는 `TRIPLE_QUARTET(3중 4중주)`를 추가하기 위해 존재하지도 않는 11명이 연주하는 더미 상수를 추가하지 않을 수 있었다.

Oracle 공식 문서에서도 대부분의 프로그래머들에게 쓸일이 없고 EnumSet이나 EnumMap 같은 자료구조를 위해 설계되어 있다고 명시되어 있다.(Most programmers will have no use for this method. It is designed for use by sophisticated enum-based data structures, such as EnumSet and EnumMap.)

---
