CREATE database TEST_MOCK;
USE TEST_MOCK;
CREATE TABLE `user_vk` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);
CREATE USER 'test_qa1' IDENTIFIED BY 'qa_test1';
GRANT ALL PRIVILEGES ON * . * TO 'test_qa1';
FLUSH PRIVILEGES;
