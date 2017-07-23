<html>

<head>
  <!-- Compiled and minified CSS -->
   <!--<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/css/materialize.min.css">

   <!-- Compiled and minified JavaScript -->
   <!--<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/js/materialize.min.js"></script>-->

</head>

<body>
  <h3> T1.p1: Chat de texto </h3>
  <div class="row">
  <ul>
  %for (n, m) in messages:
      <li> <b>{{n}}: </b> {{m}} </li>
  %end
  </ul>
  </div>

  <form action="/send" method=POST>
    <div class="row">
      <div class="input-field col s12 m6 g3">
        <input id="nome" placeholder="Nick" name="nick" type="text" value="{{nick}}"/>
      </div>
      <div class="input-field col s12 m6 g3">
        <input id="mensagem" placeholder="Mensagem" name="message" type="text" />
      </div>
      <div class="input-field col s12 m6 g3">
        <input value="Enviar" type="submit" class="waves-effect waves-light btn" />
      </div>
    </div>
  </form>
</body>

</html>
