============================
Aligo REST Client for Python
============================


.. image:: https://travis-ci.org/james-song/aligo-rest-client-python.svg?branch=master
    :target: https://travis-ci.org/james-song/aligo-rest-client-python


Python 사용자를 위한 `Aligo <https://smartsms.aligo.in/>`_ REST API 모듈입니다.

* 공식 client가 아닌 관계로 이용 중 발생한 문제에 대해 책임지지 않습니다.


설치
=======

.. code-block:: shell

    pip install aligo-rest-client


기능
=======

 - SMS 발송
 - LMS 발송
 - MMS 발송
 - 상세전송 결과 확인
 - 발송가능 건수 확인
 - 일부 에러코드 Exception 랩핑


사용법
=======

초기화
------
.. code-block:: python

    from aligo.client import Aligo

    client = Aligo(
        auth_key={발급받은 API 키},
        user_id={사용자 계정},
        is_test={테스트 모드 여부 True|False}
    )

발송
-----

.. code-block:: python

    client.sms_send(sender='01012341234', receiver='01012341234', msg='테스트 메시지')

    client.lms_send(sender='01012341234', receiver='01012341234',
        msg='테스트 메시지', title='테스트 타이틀')

    client.mms_send(sender='01012341234', receiver='01012341234',
        msg='테스트 메시지', title='테스트 타이틀', image={이미지 데이터})


상세전송 결과 확인
------------------

.. code-block:: python

    client.status(msg_id={발송후 전달받은 메시지 아이디})


발송가능 건수 확인
------------------

.. code-block:: python

    client.remain()



개발환경 및 테스트 설정
==========================

::

    pip install requests


할 일
======
- 전송내역조회
- 테스트
- 문서화
