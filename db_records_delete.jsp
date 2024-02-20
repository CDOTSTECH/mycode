<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ page import="java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Delete Records</title>
</head>
<body>

<%
    String[] recordIds = request.getParameterValues("recordIds");

    if (recordIds != null && recordIds.length > 0) {
        Connection connection = null;
        PreparedStatement preparedStatement = null;

        try {
            // Establish your database connection here
            Class.forName("com.mysql.cj.jdbc.Driver"); // Use the appropriate driver class
            connection = DriverManager.getConnection("jdbc:mysql://your-database-url", "username", "password");

            // Prepare the SQL query
            String sql = "DELETE FROM your_table WHERE id IN (" +
                    String.join(",", Arrays.copyOf(recordIds, recordIds.length)) +
                    ")";
            preparedStatement = connection.prepareStatement(sql);

            // Execute the delete query
            preparedStatement.executeUpdate();

            response.sendRedirect("deleteRecords.jsp");
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        } finally {
            // Close resources (Connection, PreparedStatement, etc.)
            try {
                if (preparedStatement != null) {
                    preparedStatement.close();
                }
                if (connection != null) {
                    connection.close();
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    } else {
        response.sendRedirect("deleteRecords.jsp");
    }
%>

<h2>Delete Records</h2>

<form action="deleteRecords.jsp" method="post">
    <c:forEach var="record" items="${records}">
        <input type="checkbox" name="recordIds" value="${record.id}">
        ${record.name}<br>
    </c:forEach>
    <br>
    <input type="submit" value="Delete Selected Records">
</form>

</body>
</html>
